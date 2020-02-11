from fastapi import APIRouter
from .doc_kwargs import doc_create_order, doc_return_order
from .schemas import RequestCreateOrder, RequestReturnOrder, ResponseCreateOrder, ResponseReturnOrder
from . import functions as funcs

router = APIRouter()


@router.post('/create_order', **doc_create_order)
async def create_order(order: RequestCreateOrder):
    kwargs = {'valid_schema_data': order.dict()}
    data = await funcs.create_order(**kwargs)
    # return ResponseReturnOrder(**data)
    return {}


@router.post('/return_order', **doc_return_order)
async def return_order(data: RequestReturnOrder):
    pass
