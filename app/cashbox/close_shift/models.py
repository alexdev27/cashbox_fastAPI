from mongoengine import Document, StringField, IntField, FloatField, \
    DateTimeField, BooleanField
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