from mongoengine import Document, DateTimeField, FloatField, \
    BooleanField, IntField, StringField, ReferenceField, DENY

from datetime import datetime
from dateutil import parser


class PayGateCashOperation(Document):
    cashID = StringField(required=True)
    amount = FloatField(required=True)  # Rubles

    meta = {'collection': 'paygate_cash_operation', 'strict': False}


class CashOperation(Document):
    creation_date = DateTimeField(default=datetime.utcnow())
    sent_to_server = BooleanField(default=False)

    cashier_name = StringField(required=True)
    cashier_id = StringField(required=True)
    document_type = IntField(required=True)
    paygate_data = ReferenceField(PayGateCashOperation, reverse_delete_rule=DENY)

    meta = {'collection': 'cash_operations', 'strict': False}

    def map_to_fields(self, data):
        paygate_data = PayGateCashOperation()
        paygate_data.amount = data['amount']
        paygate_data.cashID = data['fn_number']
        paygate_data.save()
        self.paygate_data = paygate_data
        self.creation_date = parser.parse(data['datetime'])
        self.cashier_name = data['cashier_name']
        self.cashier_id = data['cashier_id']
        self.document_type = data['document_type']

        self.save().reload()
        return self
