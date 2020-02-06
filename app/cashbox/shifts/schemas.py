from datetime import datetime
from marshmallow_mongoengine import ModelSchema, fields
from .models import PayGateOpenShift, PayGateCloseShift
from app.schemas import CashierData, DefaultSuccessResponse
from pydantic import Field


class RequestCloseShift(CashierData):
    pass


class ResponseCloseShift(DefaultSuccessResponse):
    msg: str = Field('Смена закрыта', title='Сообщение о закрытии смены')


class RequestOpenShift(CashierData):
    pass


class ResponseOpenShift(DefaultSuccessResponse):
    msg: str = Field('Смена открыта', title='Сообщение о закрытии смены')


class ResponseCurrentShiftInfo(DefaultSuccessResponse):
    shift_open_time: datetime = Field(..., title='Время открытия смены')
    total_money_in_cashbox: float = Field(..., title='Количество налички в кассе')
    shift_number: int = Field(..., title='Номер текущей смены')
    shift_total_inserted: float = Field(..., title='Общее количество внесенных наличных в смене')
    shift_total_removed: float = Field(..., title='Общее количество изъятых наличных в смене')
    shift_total_sales: float = Field(..., title='Общее количество продаж за наличку в смене')
    shift_total_returns: float = Field(..., title='Общее количество возвратов денег в смене')
    start_shift_money: float = Field(..., title='Денег в кассе на начало смены')


class DBPaygateOpenShiftSchema(ModelSchema):
    class Meta:
        model = PayGateOpenShift


class DBPaygateCloseShiftSchema(ModelSchema):
    class Meta:
        model = PayGateCloseShift
