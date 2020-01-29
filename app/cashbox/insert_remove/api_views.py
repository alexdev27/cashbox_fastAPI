from fastapi import APIRouter
from .schemas import RequestCashIn, RequestCashOut
from .doc_kwargs import doc_cash_in, doc_cash_out

router = APIRouter()


@router.post('/cash_in', **doc_cash_in)
async def insert_money(cash_in: RequestCashIn):
    pass


@router.post('/cash_out', **doc_cash_out)
async def remove_money(cash_out: RequestCashOut):
    pass
