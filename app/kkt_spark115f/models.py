from os import environ as envs

from functools import wraps
from .err_codes import check_for_err_code
from .enums import KKTInfoEnum
from comtypes.client import CreateObject, GetModule
GetModule(envs.get('SPARK_DLL') or r'C:\SPARK115f\services\UDSpark.dll')
from comtypes.gen._445B09C3_EF00_47B4_9DB0_68DDD7AA9FF1_0_1_0 import FPSpark, IFPSpark
from app.enums import DocumentTypes, PaymentChoices
from app.kkt_device.models import IKKTDevice
from app.exceptions import CashboxException
from traceback import print_tb
from sys import exc_info
from app.helpers import round_half_down

import arcus2
from pprint import pprint as pp

DEFAULT_CASHIER_PASSWORD = '22333'
DEFAULT_CASHIER_NAME = 'Mr. Printer'


def _handle_kkt_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as exc:
            msg = f'Фискальный регистратор не смог ' \
                  f'выполнить функцию ({func.__name__}) ' \
                  f'Тип ошибки: {exc.__class__.__name__} ' \
                  f'Описание: {str(exc)}'
            # pp(exc_info()[2])
            print_tb(exc_info()[2], 20)
            Spark115f.kkt_object.DeinitDevice()
            raise CashboxException(data=msg)
    return wrapper


class Spark115f(IKKTDevice):

    kkt_object = CreateObject(FPSpark, None, None, IFPSpark)

    # @staticmethod
    # @_handle_kkt_errors
    # def register_fiscal_cashier(*args, **kwargs):
    #     fio = kwargs['fiscal_cashier_fio']
    #     pswd = kwargs['fiscal_cashier_password']
    #     status = Spark115f.kkt_object.SetCashier('1', pswd, fio)
    #     sh = Spark115fHelper
    #     sh.check_for_bad_code(Spark115f.kkt_object, status)
    #     info = sh.get_fully_formatted_info(Spark115f.kkt_object)
    #     return info

    def startup(*args, **kwargs):
        # set default cashier
        Spark115f.open_comport()
        register_cashier('16', '88899', 'Mr. Printer')
        Spark115f.close_port()

    @staticmethod
    @_handle_kkt_errors
    def open_comport(*args, **kwargs):
        init_device()
        info = Spark115fHelper.get_fully_formatted_info(Spark115f.kkt_object)
        return info

    def close_port(*args, **kwargs):
        Spark115f.kkt_object.DeinitDevice()
        return {}

    @staticmethod
    @_handle_kkt_errors
    def open_shift(*args, **kwargs):
        cash_number, cashier_name = args
        register_cashier(cashier_name)
        open_shift(cash_number)
        info = Spark115fHelper.get_fully_formatted_info(Spark115f.kkt_object)
        return info

    @staticmethod
    @_handle_kkt_errors
    def close_shift(*args, **kwargs):
        cashier_name = args[0]
        apply_cashier_to_operation(cashier_name)
        close_shift()
        info = Spark115fHelper.get_fully_formatted_info(Spark115f.kkt_object)
        return info

    @staticmethod
    @_handle_kkt_errors
    def force_close_shift(*args, **kwargs):
        Spark115f.close_shift()
        return {}

    @staticmethod
    @_handle_kkt_errors
    def handle_order(*args, **kwargs):
        cashier_name = kwargs['cashier_name'] or DEFAULT_CASHIER_NAME
        p_type = kwargs['payment_type']
        d_type = kwargs['document_type']
        wares = kwargs['wares']
        money_given = int(kwargs.get('amount_entered', 0))
        pay_link = kwargs.get('pay_link', '')
        pref = kwargs.get('order_prefix', '')
        order_num = kwargs.get('order_number', 0)
        sh = Spark115fHelper

        apply_cashier_to_operation(cashier_name)

        total_price = 0
        total_price_without_discount = 0

        for ware in wares:
            total_price = round_half_down(total_price + ware['amount'], 2)
            total_price_without_discount += round_half_down(ware['quantity'] * ware['price'], 2)

        noncash_info = {}

        if DocumentTypes.PAYMENT == d_type:
            kwargs.update({'spark_doctype': 1})
        elif DocumentTypes.RETURN == d_type:
            kwargs.update({'spark_doctype': 2})

        if PaymentChoices.NON_CASH.value == p_type:
            kwargs.update({'spark_paytype': 1})
            _data = {}
            if DocumentTypes.PAYMENT == d_type:
                _data.update(arcus_purchase(int(total_price * 100)))
            elif DocumentTypes.RETURN == d_type:
                if pay_link:
                    _data.update(arcus_cancel_by_link(int(total_price*100), pay_link))

            noncash_info.update(_data)
            print_arcus_document(_data['cheque'])
        elif PaymentChoices.CASH.value == p_type:
            kwargs.update({'spark_paytype': 8})

        try:
            start_fiscal_document(kwargs['spark_doctype'])
            if DocumentTypes.PAYMENT == d_type:
                print_cheque_number(pref, order_num)

            add_wares_to_document(wares)
            money = money_given or total_price
            apply_money_to_document(kwargs['spark_paytype'], int(money*100))
            end_fiscal_document()
        except Exception:
            if PaymentChoices.NON_CASH.value == p_type:
                canceled = arcus_cancel_last_document()
                print_arcus_document(canceled['cheque'])
            raise

        check_num = sh.get_last_fiscal_doc_number(Spark115f.kkt_object)
        info = sh.get_fully_formatted_info(Spark115f.kkt_object)

        info['cashier_name'] = cashier_name
        info['transaction_sum'] = total_price
        info['check_number'] = check_num
        info['total_without_discount'] = total_price_without_discount
        info['order_num'] = order_num+1
        info['rrn'] = noncash_info.get('rrn', '')
        info['pan_card'] = noncash_info.get('pan_card', '')
        info['cardholder_name'] = noncash_info.get('cardholder_name', '')
        return info

    @staticmethod
    @_handle_kkt_errors
    def insert_remove_operation(*args, **kwargs):
        cashier_name, amount, doc_type = args
        apply_cashier_to_operation(cashier_name)

        if DocumentTypes.REMOVE == doc_type:
            func = cash_out
        elif DocumentTypes.INSERT == doc_type:
            func = cash_in
        else:
            raise ValueError('Неизвестный тип документа')

        func(8, str(amount))
        info = Spark115fHelper.get_fully_formatted_info(Spark115f.kkt_object)
        return info

    @staticmethod
    @_handle_kkt_errors
    def get_info(*args, **kwargs):
        pass


class Spark115fHelper:

    @staticmethod
    def check_for_bad_code(obj, code):
        ext_err_code = obj.GetExtendedErrorCode()
        err_msg = 'test_msg'

        if check_for_err_code(code):
            err_msg = obj.GetExtendedErrorComment(code)
        elif check_for_err_code(ext_err_code):
            err_msg = obj.GetExtendedErrorComment(ext_err_code)
        else:
            return

        raise Exception(err_msg)

    @staticmethod
    def get_fully_formatted_info(obj):
        h = Spark115fHelper
        info = {
            'is_open_shift': h.is_open_shift(obj),
            'fn_number': h.get_factory_number(obj),
            'shift_number': h.get_current_shift_number(obj),
            'inn': h.get_inn(obj),
            'datetime': h.get_current_time(obj),
            'cash_balance': h.get_current_cash_balance(obj),
            'doc_number': h.get_last_doc_number(obj)
        }
        print(info)
        return info

    @staticmethod
    def get_current_shift_number(obj):
        return int(str(obj.GetTextDeviceInfo(KKTInfoEnum.shift_number)).strip())

    @staticmethod
    def get_shift_open_close_time(obj):
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.shift_open_close_time)).strip()

    @staticmethod
    def get_current_time(obj):
        data = str(obj.GetTextDeviceInfo(KKTInfoEnum.current_time_and_date)).strip()
        return data

    @staticmethod
    def get_current_cash_balance(obj):
        return int(str(obj.GetTextDeviceInfo(KKTInfoEnum.current_cash_balance)).strip())

    @staticmethod
    def get_fiscal_memory_device_number(obj):
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.fiscal_memory_device_number)).strip()

    @staticmethod
    def get_inn(obj):
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.inn)).strip()

    @staticmethod
    def get_last_doc_number(obj):
        return int(obj.GetTextDeviceInfo(KKTInfoEnum.last_doc_number))

    @staticmethod
    def get_last_fiscal_doc_number(obj):
        return int(obj.GetTextDeviceInfo(KKTInfoEnum.last_fiscal_doc_number))

    @staticmethod
    def get_reg_number(obj):
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.reg_number)).strip()

    @staticmethod
    def get_factory_number(obj):
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.factory_number)).strip()

    @staticmethod
    def get_transaction_sum(obj):
        return int(obj.GetTextDeviceInfo(KKTInfoEnum.transaction_sum))

    @staticmethod
    def is_open_shift(obj):
        status = int(obj.ChkShift())
        Spark115fHelper.check_for_bad_code(obj, status)

        if status == -2:
            return False
        elif status == -3:
            return True


def print_cheque_number(pref, order_num):
    Spark115f.kkt_object.PrintExtraDocData(' ')
    Spark115f.kkt_object.PrintText(1, '----------------------------')
    Spark115f.kkt_object.PrintText(1, 'Номер заказа: %s' % (f'{pref}{order_num + 1}',))
    Spark115f.kkt_object.PrintText(1, '----------------------------')


def check_for_spark_error_codes(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            status = func(*args, **kwargs)
            Spark115fHelper.check_for_bad_code(Spark115f.kkt_object, status)
        except Exception:
            Spark115f.kkt_object.CancelDoc()
            raise

    return wrapper


@check_for_spark_error_codes
def register_cashier(fio,  pswd=DEFAULT_CASHIER_PASSWORD, pos='1'):
    cashier_fio = fio or 'Mr. Printer'
    return Spark115f.kkt_object.SetCashier(str(pos), str(pswd), str(cashier_fio))


def apply_cashier_to_operation(fio, pswd=DEFAULT_CASHIER_PASSWORD, pos='1'):
    register_cashier(fio, pswd, pos)
    init_cashier(pswd)


@check_for_spark_error_codes
def init_cashier(pswd=DEFAULT_CASHIER_PASSWORD):
    return Spark115f.kkt_object.RegCashier(str(pswd))


@check_for_spark_error_codes
def init_device():
    return Spark115f.kkt_object.InitDevice()


@check_for_spark_error_codes
def add_ware_to_document(item):
    return Spark115f.kkt_object.Item(*item)


def add_wares_to_document(wares):
    for ware in wares:
        item = (int(ware['quantity'] * 1000), int(ware['priceDiscount'] * 100),
                f'{ware["barcode"]} {ware["name"]}', ware['tax_number'] + 1)
        add_ware_to_document(item)
        if ware.get('discount', 0):
            Spark115f.kkt_object.PrintText(1, f'Скидка: {ware["discount"]}')


@check_for_spark_error_codes
def apply_money_to_document(pay_type, money):
    return Spark115f.kkt_object.AddPay(pay_type, str(money))


@check_for_spark_error_codes
def open_shift(cash_num, cashier_password=DEFAULT_CASHIER_PASSWORD):
    return Spark115f.kkt_object.OpenShift(int(cash_num), str(cashier_password))


@check_for_spark_error_codes
def close_shift():
    return Spark115f.kkt_object.CloseShift()


@check_for_spark_error_codes
def cash_in(cash_type, amount):
    return Spark115f.kkt_object.CashIn(cash_type, str(amount))


@check_for_spark_error_codes
def cash_out(cash_type, amount):
    return Spark115f.kkt_object.CashOut(cash_type, str(amount))


@check_for_spark_error_codes
def start_fiscal_document(doc_type):
    return Spark115f.kkt_object.StartDocSB(doc_type)


@check_for_spark_error_codes
def end_fiscal_document():
    return Spark115f.kkt_object.EndDocSB()


@check_for_spark_error_codes
def start_custom_document():
    return Spark115f.kkt_object.StartFreeDoc()


@check_for_spark_error_codes
def end_custom_document():
    return Spark115f.kkt_object.EndFreeDoc()


def print_arcus_document(strings):
    cheque = strings.split('\r')
    start_custom_document()
    for i in cheque:
        Spark115f.kkt_object.PrintText(0, i)
    end_custom_document()


# arcus methods

def arcus_check_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = func(*args, **kwargs)
        if info.get('error', False):
            raise Exception(f'Ошибка аркуса: {info}')
        return info
    return wrapper


@arcus_check_errors
def arcus_purchase(total):
    return arcus2.purchase(total)


@arcus_check_errors
def arcus_cancel_by_link(total, link):
    return arcus2.cancel_by_link(total, link)


@arcus_check_errors
def arcus_cancel_last_document():
    return arcus2.cancel_last()

