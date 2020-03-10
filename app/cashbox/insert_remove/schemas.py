from pydantic import Field

from .models import CashOperation
from app.schemas import CashierData, DefaultSuccessResponse
from marshmallow_mongoengine import ModelSchema, fields


class RequestCashIn(CashierData):
    amount: float = Field(..., title='Количество вносимых денег (в рублях)', ge=0.1)


class RequestCashOut(CashierData):
    amount: float = Field(..., title='Количество вносимых денег (в рублях)', ge=0.1)


class ResponseCashIn(DefaultSuccessResponse):
    # amount: float = Field(..., title='Сколько было внесено')
    msg: str = Field('Успешно', title='Сообщение о совершенной операции')


class ResponseCashOut(DefaultSuccessResponse):
    # amount: float = Field(..., title='Сколько было изъято')
    msg: str = Field('Успешно', title='Сообщение о совершенной операции')


class CashOperationSchema(ModelSchema):
    creation_date = fields.Str(load_from='datetime', required=True)
    cashID = fields.Str(load_from='fn_number', required=True)

    class Meta:
        model = CashOperation


