from os import environ as envs
from functools import wraps
from .err_codes import check_for_err_code, SHIFT_IS_OPEN, SHIFT_IS_CLOSED, SHIFT_IS_ELAPSED
from .enums import KKTInfoEnum
from comtypes.client import CreateObject, GetModule
from app.logging import get_logger

DLL_PATH = envs.get('SPARK_DLL', r'C:\SPARK115F\services\UDSpark.dll')
GetModule(DLL_PATH)

from comtypes.gen._445B09C3_EF00_47B4_9DB0_68DDD7AA9FF1_0_1_0 import FPSpark, IFPSpark
from app.enums import DocumentTypes, PaymentChoices
from app.kkt_device.models import IKKTDevice
from app.exceptions import CashboxException
from traceback import print_tb
from sys import exc_info
from app.helpers import round_half_down, round_half_up

import arcus2
from pprint import pprint as pp

DEFAULT_CASHIER_PASSWORD = '22333'
DEFAULT_CASHIER_NAME = 'Mr. Printer'

arcus_logger = get_logger('arcus_logs.txt', 'arcus_logger')


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
            # print_tb(exc_info()[2], 20)
            Spark115f.kkt_object.DeinitDevice()
            raise CashboxException(data=msg)
    return wrapper


def _exception_if_shift_is_elapsed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if int(Spark115f.kkt_object.ChkShift()) == SHIFT_IS_ELAPSED:
            msg = 'Смена открыта более чем 24 часа. Закройте смену и откройте снова'
            raise Exception(msg)
        return func(*args, **kwargs)
    return wrapper


class Spark115f(IKKTDevice):

    kkt_object = CreateObject(FPSpark, None, None, IFPSpark)


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
        cashier_name = args[0] if args else DEFAULT_CASHIER_NAME
        apply_cashier_to_operation(cashier_name)
        close_shift()
        try: ### Временно ###
            arcus_close_shift()
        except Exception as e:
            pass
        info = Spark115fHelper.get_fully_formatted_info(Spark115f.kkt_object)
        return info

    @staticmethod
    @_handle_kkt_errors
    def force_close_shift(*args, **kwargs):
        Spark115f.close_shift()
        return {}

    @staticmethod
    @_handle_kkt_errors
    @_exception_if_shift_is_elapsed
    def handle_order(*args, **kwargs):
        cashier_name = kwargs['cashier_name'] or DEFAULT_CASHIER_NAME
        order_num = kwargs.get('order_number', 0)
        sh = Spark115fHelper

        apply_cashier_to_operation(cashier_name)

        if PaymentChoices.CASH.value == kwargs['payment_type']:
            kwargs.update({'spark_paytype': 8})
        elif PaymentChoices.NON_CASH.value == kwargs['payment_type']:
            kwargs.update({'spark_paytype': 1})

        if DocumentTypes.PAYMENT == kwargs['document_type']:
            kwargs.update({'spark_doctype': 1})
            create_order(kwargs)
        elif DocumentTypes.RETURN == kwargs['document_type']:
            kwargs.update({'spark_doctype': 2})
            cancel_order(kwargs)

        check_num = sh.get_last_fiscal_doc_number(Spark115f.kkt_object)
        info = sh.get_fully_formatted_info(Spark115f.kkt_object)
        noncash_info = kwargs.get('arcus_data', {})

        info['cashier_name'] = cashier_name
        info['transaction_sum'] = kwargs.get('total_price', 0)
        info['check_number'] = check_num
        info['total_without_discount'] = kwargs.get('total_price_without_discount', 0)
        info['order_num'] = order_num+1
        info['rrn'] = noncash_info.get('rrn', '')
        info['pan_card'] = noncash_info.get('pan_card', '')
        info['cardholder_name'] = noncash_info.get('cardholder_name', '')
        return info

    @staticmethod
    @_handle_kkt_errors
    @_exception_if_shift_is_elapsed
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
        return int(str(obj.GetTextDeviceInfo(KKTInfoEnum.current_cash_balance)).strip()) / 100

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
        if status == SHIFT_IS_ELAPSED:
            return True
        else:
            Spark115fHelper.check_for_bad_code(obj, status)

        if status == SHIFT_IS_CLOSED:
            return False
        elif status == SHIFT_IS_OPEN:
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
        arcus_logger.info(f'=== Начало исполнения функции {func.__name__}')
        info = func(*args, **kwargs)
        if info.get('error', False):
            arcus_logger.error(f'\t====== Error ======\n'
                               f'\tОшибка при исполнении функции {func.__name__}.\n'
                               f'\tДетали ошибки: {info}')
            raise Exception(f'Ошибка аркуса: {info}')
        arcus_logger.info(f'=== Функция {func.__name__} завершилась без ошибок')
        return info
    return wrapper


@arcus_check_errors
def arcus_purchase(total):
    return arcus2.purchase(total)


@arcus_check_errors
def arcus_close_shift():
    return arcus2.close_shift() or {}


@arcus_check_errors
def arcus_cancel_by_link(total, link):
    return arcus2.cancel_by_link(total, link)


@arcus_check_errors
def arcus_cancel_last_document():
    return arcus2.cancel_last()


def create_order(kwargs):

    money_given = int(kwargs.get('amount_entered', 0) * 100)

    total_price = 0
    total_price_without_discount = 0

    for ware in kwargs['wares']:
        total_price = total_price + ware['amount']
        total_price_without_discount += ware['quantity'] * ware['price']

    total_price = round_half_down(total_price, 2)
    total_price_without_discount = round_half_down(total_price_without_discount, 2)
    pennies = int(total_price * 100)

    if kwargs['payment_type'] == PaymentChoices.CASH.value:
        process_order(money_given, kwargs)
    elif kwargs['payment_type'] == PaymentChoices.NON_CASH.value:
        kwargs.update({'arcus_data': arcus_purchase(pennies)})
        print_arcus_document(kwargs['arcus_data']['cheque'])
        process_order(pennies, kwargs)

    kwargs.update({'total_price': total_price})
    kwargs.update({'total_price_without_discount': total_price_without_discount})


def process_order(pennies, kwargs):
    try:
        start_fiscal_document(kwargs['spark_doctype'])
        if kwargs['document_type'] == DocumentTypes.PAYMENT:
            print_cheque_number(kwargs['order_prefix'], kwargs['order_number'])

        add_wares_to_document(kwargs['wares'])
        apply_money_to_document(kwargs['spark_paytype'], int(pennies))
        end_fiscal_document()
    except Exception:
        if PaymentChoices.NON_CASH.value == kwargs['payment_type']:
            canceled = arcus_cancel_last_document()
            print_arcus_document(canceled['cheque'])
        raise


def cancel_order(kwargs):
    pennies = int(kwargs['amount_entered'] * 100)
    if kwargs['payment_type'] == PaymentChoices.CASH.value:
        process_order(pennies, kwargs)
    elif kwargs['payment_type'] == PaymentChoices.NON_CASH.value:
        kwargs.update({'arcus_data': arcus_cancel_by_link(pennies, kwargs['pay_link'])})
        print_arcus_document(kwargs['arcus_data']['cheque'])
        process_order(pennies, kwargs)
