# from typing import

from pydantic import BaseModel, Field


class CashierFIOandID(BaseModel):
    cashier_id: str = Field(..., min_length=3, title='Идентификатор кассира')
    cashier_name: str = Field(..., min_length=3, title='ФИО кассира')


class RequestOpenShift(CashierFIOandID):
    pass


class RequestInsertMoney(CashierFIOandID):
    amount: float = Field(..., ge=0.5, title='Количество вносимых денег')
    # document_type
