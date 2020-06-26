from fastapi import APIRouter

from .doc_kwargs import doc_create_user
from .schemas import RequestCreateUser

users_router = APIRouter()


@users_router.post('/users', **doc_create_user)
async def create_user(data: RequestCreateUser):
    pass
