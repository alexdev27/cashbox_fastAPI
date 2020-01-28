from app.schemas import CashierData, DefaultSuccessResponse
from pydantic import Field


class RequestCloseShift(CashierData):
    pass


class ResponseCloseShift(DefaultSuccessResponse):
    msg: str = Field('Смена закрыта', title='Сообщение о закрытии смены')
