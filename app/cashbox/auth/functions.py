from typing import List

from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi import Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from config import SECRET_KEY
from .schemas import Token
from app.cashbox.users.schemas import ResponseGetUser
from app.cashbox.users.functions import get_db_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5


def login(**kwargs):
    data = kwargs['valid_schema_data']
    user = authenticate(data['login'], data['password'])
    user_dict = ResponseGetUser.from_orm(user).dict()
    token_subject = {'sub': user_dict}
    token = create_access_token(token_subject)
    return Token(access_token=token)


def authenticate(user_login, password):
    user = get_db_user(user_login)

    if not user:
        raise_incorrect_login_or_password()

    if not verify_password(password, user.password):
        raise_incorrect_login_or_password()

    return user


def _check_for_roles(roles_list: List):
    class Roles:
        def __init__(self, *args):
            self.roles = args

        def __call__(self, user=Depends(get_current_user)):
            print('user roles -------> ', user.roles)
            print('needed roles -------> ', self.roles)

    return Roles(roles_list)


def check_for_roles(*args):
    def func(user=Depends(get_current_user)):
        print('-- f1 --')
        print('args -> ', args)
        print('user roles -> ', user.roles)

    return func


# utils


def raise_incorrect_login_or_password():
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={"WWW-Authenticate": "Bearer"},
    )


def verify_password(plain_password, hashed_password):
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return bcrypt_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_subject = payload.get("sub")
        if token_subject is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = get_db_user(token_subject['login'])
    return user
