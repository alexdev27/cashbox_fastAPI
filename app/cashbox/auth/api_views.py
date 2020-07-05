from fastapi import APIRouter, Depends
from .doc_kwargs import doc_login
from . import functions
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter()


@auth_router.post('/login', **doc_login)
def login(form: OAuth2PasswordRequestForm = Depends()):
    kwargs = {'valid_schema_data': {'login': form.username, 'password': form.password}}
    return functions.login(**kwargs)
