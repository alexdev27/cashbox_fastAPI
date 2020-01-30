from fastapi import APIRouter
from .schemas import RequestCashIn, RequestCashOut, ResponseCashIn, ResponseCashOut
from .doc_kwargs import doc_cash_in, doc_cash_out, doc_test_cashbox_init
from .functions import handle_insert
from app.cashbox.main_cashbox.functions import init_cashbox

router = APIRouter()


@router.post('/cash_in', **doc_cash_in)
async def insert_money(cash_in: RequestCashIn):
    kwargs = {'valid_schema_data': cash_in.dict()}
    data = await handle_insert(**kwargs)
    return ResponseCashIn(**data)


@router.post('/cash_out', **doc_cash_out)
async def remove_money(cash_out: RequestCashOut):
    kwargs = {'valid_schema_data': cash_out}
    pass


@router.get('/test_init', **doc_test_cashbox_init)
async def test_init():
    data = await init_cashbox()
    return data