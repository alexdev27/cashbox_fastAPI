from app.utils.mongoengine_helpers import get_model_by_id_or_raise
from .models import Users
from passlib.context import CryptContext

from app.exceptions import CashboxException

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(**kwargs):
    return get_model_by_id_or_raise(Users, kwargs['user_id'])


def get_users(**kwargs):
    return {'result': list(Users.objects.all())}


def create_user(**kwargs):
    data = kwargs['valid_schema_data']
    if is_user_exist(data['login']):
        msg = f'Этот пользователь с таким логином ( {data["login"]} ) уже существует'
        raise CashboxException(data=msg, to_logging=msg)
    hash_password_if_exist(data)
    lowercase_login(data)
    return Users(**data).save()


def update_user(**kwargs):
    user_id = kwargs['user_id']
    data = kwargs['valid_schema_data']
    user = get_model_by_id_or_raise(Users, user_id)
    hash_password_if_exist(data)
    lowercase_login(data)
    user.update(**data)


def delete_user(**kwargs):
    user_id = kwargs['user_id']
    user = get_model_by_id_or_raise(Users, user_id)
    user.delete()


# utils
def hash_password_if_exist(data):
    if data.get('password'):
        data['password'] = get_hashed_password(data['password'])


def lowercase_login(data):
    data['login'] = data['login'].lower()


def is_user_exist(login):
    return bool(Users.objects(login__iexact=login).first())


def get_db_user(login):
    return Users.objects(login=login).first()

# def verify_password(plain_password, hashed_password):
#     return bcrypt_context.verify(plain_password, hashed_password)
#
#
def get_hashed_password(password):
    return bcrypt_context.hash(password)
