from mongoengine import Document, ReferenceField, DictField, \
    ListField, StringField, BooleanField, DateTimeField, IntField, UUIDField,  FloatField, DENY, URLField

from datetime import datetime


class Cashbox(Document):
    creation_date = DateTimeField(default=datetime.utcnow())
    activation_date = DateTimeField(default=datetime.utcnow()) # обновляется каждый раз при запуске приложения
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

    @staticmethod
    def set_all_inactive():
        for i in Cashbox.objects():
            i.is_active = False
            i.save()

    @staticmethod
    def box():
        # return Cashbox.objects().order_by('-activation_date').first()
        return Cashbox.objects(is_active=True).first()
