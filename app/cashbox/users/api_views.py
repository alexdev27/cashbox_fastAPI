from fastapi import APIRouter

from .doc_kwargs import doc_create_user, doc_update_user, doc_get_user, \
    doc_delete_user, doc_get_users
from .schemas import RequestCreateUser, RequestModifyUser

from . import functions

users_router = APIRouter()


@users_router.post('/users', **doc_create_user)
async def create_user(data: RequestCreateUser):
    kwargs = {'valid_schema_data': data.dict()}
    return functions.create_user(**kwargs)


@users_router.get('/users/{user_id}', **doc_get_user)
def get_user(user_id: str):
    kwargs = {'user_id': user_id}
    return functions.get_user(**kwargs)


@users_router.get('/users', **doc_get_users)
def get_users():
    return functions.get_users()


@users_router.put('/users/{user_id}', **doc_update_user)
def update_user(user_id: str, data: RequestModifyUser):
    kwargs = {'user_id': user_id, 'valid_schema_data': data.dict(exclude_none=True, exclude_unset=True)}
    functions.update_user(**kwargs)


@users_router.delete('/users/{user_id}', **doc_delete_user)
def delete_user(user_id: str):
    kwargs = {'user_id': user_id}
    functions.delete_user(**kwargs)
