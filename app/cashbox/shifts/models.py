
from mongoengine import Document, ReferenceField, DictField, \
    ListField, StringField, BooleanField, DateTimeField, IntField, FloatField, DENY

from datetime import datetime
from dateutil import parser
# from app.cashbox.main_cashbox.models import Cashbox

# class CloseShift(Document):
#     # поля для внутреннего использования
#     creation_date = DateTimeField(default=datetime.utcnow())
#     sent_to_server = BooleanField(default=False)
#     #
#     cashID = StringField(required=True)
#     docNumber = IntField(required=True)
#     cashBalanceClose = FloatField(required=True)
#     totalSellClose = FloatField(required=True)
#     totalReturnClose = FloatField(required=True)
#     inAmount = FloatField(required=True)
#     outAmount = FloatField(required=True)
#     inCount = IntField(required=True)
#     outCount = IntField(required=True)
#     discountAmount = FloatField(required=True)
#     discountReturns = FloatField(required=True)
#     amount = FloatField(required=True)
#     returns = FloatField(required=True)
#     meta = {'collection': 'closed_shifts', 'strict': False, 'indexes': ['cashID']}

#
# class OpenShift(Document):
#     # поля для внутреннего использования
#     creation_date = DateTimeField(default=datetime.utcnow())
#     sent_to_server = BooleanField(default=False)
#     closed = BooleanField(default=False)
#     # orders = ListField(ReferenceField(Order, reverse_delete_rule=DENY), default=[])
#     # in_out_operations = ListField(ReferenceField(InOutCashOperation, reverse_delete_rule=DENY), default=[])
#     all_money_were_taken = BooleanField(default=False)
#
#     total_inserted_money_in_shift = FloatField(default=0)
#     total_removed_money_in_shift = FloatField(default=0)
#     total_sales_in_shift = FloatField(default=0)
#     total_returns_in_shift = FloatField(default=0)
#     start_shift_money = FloatField(default=0)
#     #####
#     # инфа на сервис платежного шлюза
#     cashID = StringField(required=True)
#     cashier = StringField(required=True)
#     cashierID = StringField(required=True)
#     shop = IntField(required=True)
#     cashNumber = IntField(required=True)
#     shiftNumber = IntField(required=True)
#     cashBalanceOpen = FloatField(required=True)
#     inn = StringField(required=True)
#     totalSellOpen = FloatField(required=True)
#     totalReturnOpen = FloatField(required=True)
#     cashName = StringField(required=True)
#     cashSerial = StringField(required=True)
#     meta = {'collection': 'opened_shifts', 'strict': False, 'indexes': ['cashID']}



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
    # orders = ListField(ReferenceField(Order, reverse_delete_rule=DENY), default=[])
    # in_out_operations = ListField(ReferenceField(InOutCashOperation, reverse_delete_rule=DENY), default=[])
    paygate_data = ReferenceField(PayGateOpenShift, reverse_delete_rule=DENY)

    meta = {'collection': 'opened_shifts', 'strict': False}

    def map_to_fields(self, kwargs):
        self.cashier_name = kwargs['cashier_name']
        self.cashier_id = kwargs['cashier_id']
        self.start_shift_money = kwargs['cash_balance']
        self.creation_date = parser.parse(kwargs['datetime'])

        paygate_data = PayGateOpenShift()
        paygate_data.cashID = kwargs['fn_number']
        paygate_data.cashier = kwargs['cashier_name']
        paygate_data.cashierID = kwargs['cashier_id']
        paygate_data.shop = kwargs['shop_number']
        paygate_data.cashNumber = kwargs['cash_number']
        paygate_data.shiftNumber = kwargs['shift_number']
        paygate_data.cashBalanceOpen = kwargs['cash_balance']
        paygate_data.inn = kwargs['inn']
        paygate_data.totalSellOpen = kwargs['progressive_total_sales']
        paygate_data.totalReturnOpen = kwargs['progressive_total_returns']
        paygate_data.cashName = kwargs['cash_name']
        paygate_data.cashSerial = kwargs['fn_number']
        paygate_data.proj = kwargs['project_number']
        paygate_data.systemID = kwargs['system_id']
        paygate_data.save()
        self.paygate_data = paygate_data
        self.save().reload()
        return self
