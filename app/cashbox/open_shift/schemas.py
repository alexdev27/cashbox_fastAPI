from app.schemas import CashierData, DefaultSuccessResponse
from pydantic import Field


class RequestOpenShift(CashierData):
    pass


class ResponseOpenShift(DefaultSuccessResponse):
    msg: str = Field('Смена открыта', title='Сообщение о закрытии смены')
