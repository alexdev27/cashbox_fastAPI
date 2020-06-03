from typing import Dict

from mongoengine import Document, ReferenceField, DictField, \
    ListField, StringField, BooleanField, DateTimeField, IntField, DENY

from uuid import uuid4
from app.cashbox.orders.models import Order
from app.cashbox.shifts.models import OpenShift, CloseShift
from app.enums import DocumentTypes
from datetime import datetime
from app.helpers import round_half_up


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
    closed_shifts = ListField(ReferenceField(CloseShift, reverse_delete_rule=DENY), default=[])
    current_opened_shift = ReferenceField(OpenShift, reverse_delete_rule=DENY, default=None)

    # data_to_send = ListField(DictField(default={}), default=[])
    meta = {'collection': 'cashbox', 'strict': False}

    @staticmethod
    def set_all_inactive():
        for i in Cashbox.objects():
            i.is_active = False
            i.save()

    @staticmethod
    def box():
        return Cashbox.objects(is_active=True).first()

    def save_paygate_data_for_send(self, data: Dict):
        DataToPayGate(data=data).save()

    def modify_shift_order_number(self):
        self.current_opened_shift.order_number += 1
        self.current_opened_shift.save()

    def get_shift_order_number(self):
        return self.current_opened_shift.order_number

    def set_current_shift(self, shift: OpenShift):
        shift.save().reload()
        self.current_opened_shift = shift
        self.save()

    def close_shift(self, shift: CloseShift):
        shift.save().reload()
        self.closed_shifts.append(shift)
        self.current_opened_shift.closed = True
        self.current_opened_shift.save()
        self.current_opened_shift = None
        self.save()

    def add_cash_operation_to_shift(self, cash_operation):
        cash_operation.save().reload()
        self.current_opened_shift.in_out_operations.append(cash_operation)
        self.current_opened_shift.save()

    def update_shift_money_counter(self, operation_number, amount):
        # Big badass if statement
        shift = self.current_opened_shift
        r_func = round_half_up

        print('amount incoming -> ', amount, ' op_number -> ', operation_number)

        if operation_number == DocumentTypes.INSERT:
            shift.total_inserted_money_in_shift = r_func(shift.total_inserted_money_in_shift + amount, 2)
        elif operation_number == DocumentTypes.REMOVE:
            shift.total_removed_money_in_shift = r_func(shift.total_removed_money_in_shift + amount, 2)
        elif operation_number == DocumentTypes.PAYMENT:
            shift.total_sales_in_shift = r_func(shift.total_sales_in_shift + amount, 2)
        elif operation_number == DocumentTypes.RETURN:
            shift.total_returns_in_shift = r_func(shift.total_returns_in_shift + amount, 2)

        shift.save().reload('total_inserted_money_in_shift', 'total_removed_money_in_shift',
                            'total_sales_in_shift', 'total_returns_in_shift')

    def add_order(self, order: Order):
        shift = self.current_opened_shift
        shift.orders.append(order)
        order.save()
        shift.save()


class DataToPayGate(Document):
    creation_date = DateTimeField(default=datetime.utcnow())
    data = DictField(required=True)

    meta = {'collection': 'to_paygate', 'strict': False, 'ordering': ['creation_date']}


class System(Document):
    system_uuid = StringField(required=True)

    meta = {'collection': 'system_id', 'strict': False}

    @staticmethod
    def get_sys_id():
        obj = System._get_or_create()
        return obj.system_uuid

    @staticmethod
    def _get_or_create():
        if list(System.objects()):
            return System.objects().first()
        else:
            return System(system_uuid=str(uuid4())).save().reload()
