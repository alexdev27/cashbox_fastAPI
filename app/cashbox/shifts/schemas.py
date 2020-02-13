from datetime import datetime
from marshmallow_mongoengine import ModelSchema, fields
from .models import OpenShift, CloseShift
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


class OpenShiftSchema(ModelSchema):
    start_shift_money = fields.Float(load_from='cash_balance')
    creation_date = fields.DateTime(load_from='datetime', required=True)

    cashID = fields.Str(load_from='fn_number', required=True)
    cashier = fields.Str(load_from='cashier_name', required=True)
    cashierID = fields.Str(load_from='cashier_id', required=True)
    shop = fields.Int(load_from='shop_number', required=True)
    cashNumber = fields.Int(load_from='cash_number', required=True)
    shiftNumber = fields.Int(load_from='shift_number', required=True)
    cashBalanceOpen = fields.Float(load_from='cash_balance', required=True)
    inn = fields.Str(load_from='inn', required=True)
    totalSellOpen = fields.Float(load_from='progressive_total_sales', required=True)
    totalReturnOpen = fields.Float(load_from='progressive_total_returns', required=True)
    cashName = fields.Str(load_from='cash_name', required=True)
    cashSerial = fields.Str(load_from='fn_number', required=True)
    systemID = fields.Str(load_from='system_id', required=True)
    proj = fields.Int(load_from='project_number', required=True)

    class Meta:
        model = OpenShift

    @staticmethod
    def get_data_for_paygate(shift_object):
        _fields = [
            'cashID', 'cashier', 'cashierID', 'shop',
            'cashNumber', 'shiftNumber', 'cashBalanceOpen',
            'inn', 'totalSellOpen', 'totalReturnOpen',
            'cashName', 'cashSerial', 'systemID', 'proj',
        ]
        return OpenShiftSchema(only=_fields).dump(shift_object).data


class CloseShiftSchema(ModelSchema):
    creation_date = fields.DateTime(load_from='datetime', required=True)
    cashID = fields.Str(load_from='fn_number', required=True)
    docNumber = fields.Int(load_from='doc_number', required=True)
    cashBalanceClose = fields.Float(load_from='cash_balance', required=True)
    totalSellClose = fields.Float(load_from='progressive_total_sales', required=True)
    totalReturnClose = fields.Float(load_from='progressive_total_returns', required=True)
    inAmount = fields.Float(load_from='sum_insert', required=True)
    outAmount = fields.Float(load_from='sum_remove', required=True)
    inCount = fields.Int(load_from='count_insert', required=True)
    outCount = fields.Int(load_from='count_remove', required=True)
    discountAmount = fields.Float(load_from='discount_sum_sales', required=True)
    discountReturns = fields.Float(load_from='discount_sum_returns', required=True)
    amount = fields.Float(load_from='sum_sales', required=True)
    returns = fields.Float(load_from='sum_returns', required=True)

    class Meta:
        model = CloseShift

    @staticmethod
    def get_data_for_paygate(shift_object):
        _fields = ['cashier_name', 'cashier_id', 'creation_date']
        return CloseShiftSchema(exclude=_fields).dump(shift_object).data
