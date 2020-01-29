
from mongoengine import Document, ReferenceField, DictField, \
    ListField, StringField, BooleanField, DateTimeField, IntField, FloatField, DENY

from datetime import datetime


class CloseShift(Document):
    # поля для внутреннего использования
    creation_date = DateTimeField(default=datetime.utcnow())
    sent_to_server = BooleanField(default=False)
    #
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
    meta = {'collection': 'closed_shifts', 'strict': False, 'indexes': ['cashID']}


class OpenShift(Document):
    # поля для внутреннего использования
    creation_date = DateTimeField(default=datetime.utcnow())
    sent_to_server = BooleanField(default=False)
    closed = BooleanField(default=False)
    # orders = ListField(ReferenceField(Order, reverse_delete_rule=DENY), default=[])
    # in_out_operations = ListField(ReferenceField(InOutCashOperation, reverse_delete_rule=DENY), default=[])
    all_money_were_taken = BooleanField(default=False)

    total_inserted_money_in_shift = FloatField(default=0)
    total_removed_money_in_shift = FloatField(default=0)
    total_sales_in_shift = FloatField(default=0)
    total_returns_in_shift = FloatField(default=0)
    start_shift_money = FloatField(default=0)
    #####
    # инфа на сервис платежного шлюза
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
    meta = {'collection': 'opened_shifts', 'strict': False, 'indexes': ['cashID']}
