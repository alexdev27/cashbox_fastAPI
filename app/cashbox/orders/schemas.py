from typing import List
from datetime import datetime
from pydantic import Field, BaseModel, validator
from app.enums import PaymentChoices, DocumentTypes, CashboxTaxesNumbers
from app.schemas import DefaultSuccessResponse, CashierData
from .models import Ware, Order
from marshmallow_mongoengine import ModelSchema, fields
from marshmallow import Schema, post_load
from app.cashbox.main_cashbox.models import Cashbox


class RequestWares(BaseModel):
    name: str = Field(..., title='Название товара', min_length=3)
    barcode: str = Field(..., title='Баркод товара', min_length=4)
    code: str = Field(..., title='Локальный код товара', min_length=4)
    quantity: int = Field(..., title='Количество', ge=1)
    price: float = Field(..., title='Цена товара', ge=0.5)
    tax_rate: CashboxTaxesNumbers = Field(..., title='Налоговаяя ставка')
    # tax_number: FiscalTaxesNumbers = Field(..., title='Номер налога (настоящий номер налога в фискальном регистраторе)')


class RequestCreateOrder(BaseModel):
    cashier_name: str = Field('', title='ФИО даныые кассира. Возмется из текущей смены, если не передано')
    cashier_id: str = Field('', title='Идентификатор кассира. Возмется из текущей смены, если не передано')

    payment_type: PaymentChoices = Field(..., title='Тип оплаты (наличный/безналичный)')
    amount_entered: float = Field(0, title='Если наличный расчет, то это поле показывает сколько денег дал клиент')
    wares: List[RequestWares] = Field(..., title='Список позиций в покупке', min_items=1)

    @validator('amount_entered', always=True)
    def nonzero_amount_entered(cls, v, values, **kwargs):
        if values['payment_type'] == PaymentChoices.CASH:
            if v <= 0 or isinstance(v, type(None)):
                raise ValueError(f'amount_entered must be greater than zero, '
                                 f'if it is payment with real money')
        return v

    # quick hack to check cashier fields
    # @validator('payment_type')
    # def check_cashier(cls, v, values, **kwargs):
    #     if bool(values.get('cashier_id', '')) and bool(values.get('cashier_name', '')):
    #         return v
    #     else:
    #         shift = Cashbox.box().current_opened_shift
    #         values['cashier_name'] = shift.cashier
    #         values['cashier_id'] = shift.cashierID
    #     return v


class ResponseCreateOrder(DefaultSuccessResponse):
    internal_order_uuid: str = Field(..., title='Уникальный идентификатор заказа в кассе', min_length=9)
    cheque_number: int = Field(..., title='Номер созданного чека', gt=0)
    payment_type: PaymentChoices = Field(..., title='Тип оплаты (наличный/безналичный)')
    document_type: int = Field(DocumentTypes.PAYMENT, title='Тип документа (оплата)')
    cashier_name: str = Field(..., title='ФИО кассира')
    payment_link: str = Field("", title='Ссылка платежа (пустая, если наличный расчет)')
    order_time: str = Field(..., title='Время заказа (из фискального регистратора). Пример: "2020-01-28 09:00:27"')
    cash_character: str = Field(..., title='Символ кассы. Необходим для совершения заказа/оплаты', min_length=1)
    device_id: str = Field(..., title='Идентификатор устройства (кассы)', min_length=4)


class RequestReturnOrder(CashierData):
    internal_order_uuid: str = Field(..., title='Уникальный идентификатор заказа в кассе', min_length=9)
    # payment_link: str = Field("", title='Ссылка платежа (пустая, если возврат по наличному платежу)')


class ResponseReturnOrder(DefaultSuccessResponse):
    msg: str = Field('Заказ отменен', title='Сообщение об успешной отмене')


# class RequestRoundPrice(RequestWares):
#     pass


class ResponseRoundPrice(DefaultSuccessResponse):
    barcode: str = Field(..., title='Баркод округлённого товара')
    discountedPrice: float = Field(..., title='Сумма позиции со скидкой')
    discountedSum: float = Field(..., title='Сумма скидки')
    orderSum: float = Field(..., title='Сумма заказа без скидки')
    discountedOrderSum: float = Field(..., title='Сумма заказа со скидкой')


class WareSchema(ModelSchema):
    class Meta:
        model = Ware


class OrderSchema(ModelSchema):
    creation_date = fields.Str(required=True)
    wares = fields.Nested(WareSchema, many=True)

    class Meta:
        model = Order


class PaygateWareSchema(ModelSchema):
    class Meta:
        model = Ware
        model_build_obj = False
        exclude = ['tax_number']


class PaygateOrderSchema(ModelSchema):
    wares = fields.Nested(PaygateWareSchema, many=True)

    class Meta:
        model = Order
        model_build_obj = False
        fields = ['clientOrderID', 'cardHolder', 'pan', 'payLink',
                  'amount', 'payType', 'paid', 'cashID', 'checkNumber', 'wares']


class ConvertToResponseCreateOrder(Schema):
    internal_order_uuid = fields.Str(required=True, load_from='clientOrderID')
    cheque_number = fields.Int(required=True, load_from='checkNumber')
    payment_type = fields.Int(required=True, load_from='payType')
    document_type = fields.Int(required=True)
    cashier_name = fields.Str(required=True)
    payment_link = fields.Str(default='', load_from='payLink')
    order_time = fields.Str(required=True, load_from='creation_date')
    cash_character = fields.Str(required=True, load_from='order_prefix')
    device_id = fields.Str(required=True)

    @post_load
    def modify_time(self, data):
        data['order_time'] = str(data['order_time']).replace('T', ' ')
        return data
