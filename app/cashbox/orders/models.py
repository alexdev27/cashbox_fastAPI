
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
    tax_number = IntField(required=True)
    taxRate = FloatField(required=True)
    taxSum = FloatField(required=True)
    amount = FloatField(required=True)
    department = IntField(required=True)
    posNumber = IntField(required=True)
    meta = {'collection': 'wares', 'strict': False, 'indexes': ['barcode']}


class Order(Document):
    # поля для внутреннего использования
    creation_date = DateTimeField(default=datetime.utcnow())
    return_date = DateTimeField()
    sent_to_server = BooleanField(default=False)
    returned = BooleanField(default=False)
    cashier_name = StringField(required=True)
    cashier_id = StringField(required=True)
    return_cashier_name = StringField(default='')
    return_cashier_id = StringField(default='')
    order_prefix = StringField(required=True)
    order_number = IntField(required=True)

    #
    clientOrderID = StringField(required=True)
    cardHolder = StringField(default='')
    pan = StringField(default='')
    payLink = StringField(default='')

    amount = FloatField(required=True)
    amount_with_discount = FloatField(required=True)
    payType = IntField(required=True)
    paid = IntField(required=True)
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

