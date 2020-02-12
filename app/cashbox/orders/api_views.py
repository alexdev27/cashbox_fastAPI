from fastapi import APIRouter
from .doc_kwargs import doc_create_order, doc_return_order
from .schemas import RequestCreateOrder, RequestReturnOrder, ResponseCreateOrder, ResponseReturnOrder
from . import functions as funcs

router = APIRouter()


@router.post('/create_order', **doc_create_order)
async def create_order(order: RequestCreateOrder):
    kwargs = {'valid_schema_data': order.dict()}
    data = await funcs.create_order(**kwargs)
    return ResponseCreateOrder(**data)


@router.post('/return_order', **doc_return_order)
async def return_order(order: RequestReturnOrder):
    kwargs = {'valid_schema_data': order.dict()}
    data = await funcs.return_order(**kwargs)
    return {}
    # return ResponseReturnOrder(**data)
