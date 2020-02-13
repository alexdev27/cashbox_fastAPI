from mongoengine import Document, DateTimeField, StringField
from datetime import datetime


class CommonFieldsMixin(Document):
    cashier_name = StringField(required=True)
    cashier_id = StringField(required=True)
    creation_date = DateTimeField(default=datetime.utcnow())
    meta = {'abstract': True}
