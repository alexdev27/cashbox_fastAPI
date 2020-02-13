
from mongoengine import Document, ReferenceField, DictField, \
    ListField, StringField, BooleanField, DateTimeField, IntField, FloatField, DENY
from app.cashbox.insert_remove.models import CashOperation
from datetime import datetime
from dateutil import parser

from app.cashbox.orders.models import Order


class PayGateOpenShift(Document):
    cashID = StringField(required=True)
    cashier = StringField(required=True)
    cashierID = StringField(required=True)
    shop = IntField(required=True)
    cashNumber = IntField(required=True)
    shiftNumber = IntField(required=True)
    cashBalanceOpen = FloatField(required=True)
    inn = StringField(required=True)
    totalSellOpen = FloatField(required=True)
    totalReturnOpen = FloatField(required=True)
    cashName = StringField(required=True)
    cashSerial = StringField(required=True)
    systemID = StringField(required=True)
    proj = IntField(required=True)
    meta = {'collection': 'paygate_open_shift',
            'strict': False, 'indexes': ['cashID']}


class PayGateCloseShift(Document):
    cashID = StringField(required=True)
    docNumber = IntField(required=True)
    cashBalanceClose = FloatField(required=True)
    totalSellClose = FloatField(required=True)
    totalReturnClose = FloatField(required=True)
    inAmount = FloatField(required=True)
    outAmount = FloatField(required=True)
    inCount = IntField(required=True)
    outCount = IntField(required=True)
    discountAmount = FloatField(required=True)
    discountReturns = FloatField(required=True)
    amount = FloatField(required=True)
    returns = FloatField(required=True)
    meta = {'collection': 'paygate_close_shift',
            'strict': False, 'indexes': ['cashID']}


class OpenShift(Document):
    cashier_name = StringField(required=True)
    cashier_id = StringField(required=True)
    creation_date = DateTimeField(default=datetime.utcnow())
    closed = BooleanField(default=False)
    total_inserted_money_in_shift = FloatField(default=0)
    total_removed_money_in_shift = FloatField(default=0)
    total_sales_in_shift = FloatField(default=0)
    total_returns_in_shift = FloatField(default=0)
    start_shift_money = FloatField(default=0)
    orders = ListField(ReferenceField(Order, reverse_delete_rule=DENY), default=[])
    in_out_operations = ListField(ReferenceField(CashOperation, reverse_delete_rule=DENY), default=list())
    paygate_data = ReferenceField(PayGateOpenShift, reverse_delete_rule=DENY)

    meta = {'collection': 'opened_shifts', 'strict': False}

    def map_to_fields(self, data):
        self.cashier_name = data['cashier_name']
        self.cashier_id = data['cashier_id']
        self.start_shift_money = data['cash_balance']
        self.creation_date = parser.parse(data['datetime'])

        paygate_data = PayGateOpenShift()
        paygate_data.cashID = data['fn_number']
        paygate_data.cashier = data['cashier_name']
        paygate_data.cashierID = data['cashier_id']
        paygate_data.shop = data['shop_number']
        paygate_data.cashNumber = data['cash_number']
        paygate_data.shiftNumber = data['shift_number']
        paygate_data.cashBalanceOpen = float(data['cash_balance'])
        paygate_data.inn = data['inn']
        paygate_data.totalSellOpen = float(data['progressive_total_sales'])
        paygate_data.totalReturnOpen = float(data['progressive_total_returns'])
        paygate_data.cashName = data['cash_name']
        paygate_data.cashSerial = data['fn_number']
        paygate_data.proj = data['project_number']
        paygate_data.systemID = data['system_id']
        paygate_data.save()
        self.paygate_data = paygate_data
        self.save().reload()
        return self


class CloseShift(Document):
    cashier_name = StringField(required=True)
    cashier_id = StringField(required=True)
    creation_date = DateTimeField(default=datetime.utcnow())

    paygate_data = ReferenceField(PayGateCloseShift, reverse_delete_rule=DENY)

    meta = {'collection': 'closed_shifts', 'strict': False}

    def map_to_fields(self, data):

        self.cashier_name = data['cashier_name']
        self.cashier_id = data['cashier_id']
        self.creation_date = parser.parse(data['datetime'])

        shift = PayGateCloseShift()
        shift.cashID = data['fn_number']
        shift.docNumber = data['doc_number']
        shift.cashBalanceClose = data['cash_balance']
        shift.totalSellClose = float(data['progressive_total_sales'])
        shift.totalReturnClose = float(data['progressive_total_returns'])
        shift.inAmount = data['sum_insert']
        shift.outAmount = data['sum_remove']
        shift.inCount = data['count_insert']
        shift.outCount = data['count_remove']
        shift.discountAmount = data['discount_sum_sales']
        shift.discountReturns = data['discount_sum_returns']
        shift.amount = float(data['sum_sales'])
        shift.returns = data['sum_returns']
        shift.save()
        self.paygate_data = shift
        self.save()
        return self
