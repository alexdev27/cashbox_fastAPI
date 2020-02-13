from app.mixins import CommonFieldsMixin
from mongoengine import Document, ReferenceField, DictField, \
    ListField, StringField, BooleanField, DateTimeField, IntField, FloatField, DENY
from app.cashbox.insert_remove.models import CashOperation

from app.cashbox.orders.models import Order


class OpenShift(Document):
    creation_date = DateTimeField(required=True)
    closed = BooleanField(default=False)
    total_inserted_money_in_shift = FloatField(default=0)
    total_removed_money_in_shift = FloatField(default=0)
    total_sales_in_shift = FloatField(default=0)
    total_returns_in_shift = FloatField(default=0)
    start_shift_money = FloatField(default=0)
    orders = ListField(ReferenceField(Order, reverse_delete_rule=DENY), default=[])
    in_out_operations = ListField(ReferenceField(CashOperation, reverse_delete_rule=DENY), default=list())
    #
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

    meta = {'collection': 'opened_shifts', 'strict': False}


class CloseShift(CommonFieldsMixin):
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

    meta = {'collection': 'closed_shifts', 'strict': False}
