from fastapi import APIRouter
from .doc_kwargs import doc_create_order, doc_return_order
from .schemas import RequestCreateOrder, RequestReturnOrder

router = APIRouter()


@router.post('/create_order', **doc_create_order)
async def create_order(data: RequestCreateOrder):
    pass


@router.post('/return_order', **doc_return_order)
async def return_order(data: RequestReturnOrder):
    pass
