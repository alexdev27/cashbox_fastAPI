from pydantic import Field
from app.schemas import CashierData, DefaultSuccessResponse
from marshmallow_mongoengine import ModelSchema, fields
from .models import PayGateCashOperation


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


class DBPaygateCashOperation(ModelSchema):
    class Meta:
        model = PayGateCashOperation


class DBPaygateCashInSchema(DBPaygateCashOperation):
    pass


class DBPaygateCashOutSchema(DBPaygateCashOperation):
    pass
