
from mongoengine import Document, ReferenceField, DictField, \
    ListField, StringField, BooleanField, DateTimeField, IntField, UUIDField,  FloatField, DENY, URLField
from datetime import datetime


class Ware(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    quantity = FloatField(required=True)
    measure = StringField(default='г')
    code = StringField(required=True)
    barcode = StringField(required=True)
    priceDiscount = FloatField(required=True)
    discount = FloatField(default=0)
    taxRate = FloatField(required=True)
    taxSum = FloatField(required=True)
    amount = FloatField(required=True)
    department = IntField(default=1)
    meta = {'collection': 'wares', 'strict': False, 'indexes': ['barcode']}


class Order(Document):
    # поля для внутреннего использования
    creation_date = DateTimeField(default=datetime.utcnow())
    sent_to_server = BooleanField(default=False)
    returned = BooleanField(default=False)
    cashier_name = StringField(required=True)
    cashier_id = StringField(required=True)
    #
    clientOrderID = StringField(default='')
    cardHolder = StringField(default='')
    pan = StringField(default='')
    payLink = StringField(default='')

    amount = FloatField(required=True)
    payType = IntField(required=True)
    payd = IntField(required=True)
    cashID = StringField(required=True)
    checkNumber = IntField(required=True)
    doc_number = IntField(required=True)
    wares = ListField(ReferenceField(Ware, reverse_delete_rule=DENY), default=[])
    meta = {'collection': 'orders', 'strict': False, 'indexes': ['cashID', 'clientOrderID']}

    def save(self, **kwargs):
        for ware in self.wares:
            ware.save()
        super().save(**kwargs)
        return self

    def mark_as_returned(self):
        self.returned = True
        self.save()

