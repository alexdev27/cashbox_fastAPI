from fastapi import APIRouter
from .schemas import RequestCashIn, ResponseCashIn
from .doc_kwargs import doc_cash_in

router = APIRouter()


@router.post('/cash_in', **doc_cash_in)
def insert_money(cash_in: RequestCashIn):
    pass


def remove_money():
    pass
