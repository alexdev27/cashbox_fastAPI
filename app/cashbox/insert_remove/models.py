from mongoengine import FloatField, IntField, StringField

from app.mixins import CommonFieldsMixin


class CashOperation(CommonFieldsMixin):
    document_type = IntField(required=True)
    cashID = StringField(required=True)
    amount = FloatField(required=True)
    meta = {'collection': 'cash_operations', 'strict': False}