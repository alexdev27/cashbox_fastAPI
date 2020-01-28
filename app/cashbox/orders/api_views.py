from fastapi import APIRouter
from .doc_kwargs import doc_create_order
from .schemas import RequestCreateOrder

router = APIRouter()


@router.post('/create_order', **doc_create_order)
def close_current_shift(data: RequestCreateOrder):
    pass
