from mongoengine import DateTimeField, StringField, \
    BooleanField, ListField, ReferenceField, Document, IntField, DictField, DENY
from datetime import datetime


class Cashbox(Document):
    creation_date = DateTimeField(default=datetime.utcnow())
    activation_date = DateTimeField(default=datetime.utcnow())  # обновляется каждый раз при запуске приложения
    is_active = BooleanField(default=True)
    shop = IntField(required=True)
    cash_number = IntField(default=0)
    cash_name = StringField(required=True)
    cash_character = StringField()
    cash_id = StringField(required=True)
    project_number = IntField(default=1)
    # closed_shifts = ListField(ReferenceField(CloseShift, reverse_delete_rule=DENY), default=[])
    # current_opened_shift = ReferenceField(OpenShift, reverse_delete_rule=DENY, default=None)

    # data_to_send = ListField(DictField(default={}), default=[])
    meta = {'collection': 'cashbox', 'strict': False}
