from mongoengine import Document, DateTimeField, FloatField, \
    BooleanField, IntField, StringField
from datetime import datetime


class CashOperation(Document):
    creation_date = DateTimeField(default=datetime.utcnow())
    sent_to_server = BooleanField(default=False)

    amount = FloatField(required=True)  # Rubles
    cashier_name = StringField(required=True)
    cashier_id = StringField(required=True)
    document_type = IntField(required=True)
