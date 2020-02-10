from mongoengine import Document, DateTimeField, FloatField, \
    BooleanField, IntField, StringField
from datetime import datetime
from dateutil import parser


class CashOperation(Document):
    creation_date = DateTimeField(default=datetime.utcnow())
    sent_to_server = BooleanField(default=False)

    amount = FloatField(required=True)  # Rubles
    cashier_name = StringField(required=True)
    cashier_id = StringField(required=True)
    document_type = IntField(required=True)

    def map_to_fields(self, data):
        self.creation_date = parser.parse(data['operation_time'])
        self.amount = data['amount']
        self.cashier_name = data['cashier_name']
        self.cashier_id = data['cashier_id']
        self.document_type = data['doc_type']
        self.save().reload()
        return self
