from typing import Union, Dict, List

from pydantic import Field, BaseModel
from app.schemas import CashierData, DefaultSuccessResponse


class RequestCashIn(CashierData):
    amount: float = Field(..., title='Количество вносимых денег (в рублях)', ge=0.5)


class RequestCashOut(CashierData):
    amount: float = Field(..., title='Количество вносимых денег (в рублях)', ge=0.5)


class ResponseCashIn(DefaultSuccessResponse):
    amount: float = Field(..., title='Сколько было внесено')
    msg: float = Field(..., title='Сообщение о совершенной операции')


class ResponseCashOut(DefaultSuccessResponse):
    amount: float = Field(..., title='Сколько было изъято')
    msg: float = Field(..., title='Сообщение о совершенной операции')

