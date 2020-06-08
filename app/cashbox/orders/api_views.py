from typing import List
from fastapi import APIRouter
from .doc_kwargs import doc_create_order, doc_return_order, doc_round_price, doc_partial_return
from .schemas import RequestCreateOrder, RequestReturnOrder, \
    ResponseCreateOrder, ResponseReturnOrder, RequestWares, \
    ResponseRoundPrice, ResponsePartialReturn, RequestPartialReturn
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
    return ResponseReturnOrder(**data)


@router.post('/round_price', **doc_round_price)
async def round_price(wares: List[RequestWares]):
    kwargs = {'valid_schema_data': [ware.dict() for ware in wares]}
    data = await funcs.round_price(**kwargs)
    return ResponseRoundPrice(**data)


@router.post('/partial_return', **doc_partial_return)
async def partial_return(order: RequestPartialReturn):
    kwargs = {'valid_schema_data': order.dict()}
    data = await funcs.partial_return(**kwargs)
    return ResponsePartialReturn(**data)
