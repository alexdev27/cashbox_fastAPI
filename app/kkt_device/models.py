import copy
from functools import wraps
from config import CASH_SETTINGS as CS
import cashbox as real_kkt
from app.exceptions import CashboxException


def _handle_kkt_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result.get('error'):
                msg = f'Ошибка при открытии порта: {result["message"]}'
                raise CashboxException(data=msg)
            if result.get('status_printer_error_code'):
                if result['status_printer_error_code'] > 0:
                    code = result['status_printer_error_code']
                    err_msg = result['status_printer_message']
                    msg = f'Ошибка фискального регистратора: ' \
                          f'Код: {code} Сообщение: {err_msg}'
                    raise CashboxException(data=msg)
            return result
        except Exception as exc:
            msg = f'Фискальный регистратор не смог ' \
                  f'выполнить функцию ({func.__name__}) ' \
                  f'Тип ошибки: {exc.__class__.__name__} ' \
                  f'Описание: {str(exc)}'
            raise CashboxException(data=msg)
    return wrapper


class KKTDevice:

    @staticmethod
    @_handle_kkt_errors
    def open_comport(*args, **kwargs):
        return real_kkt.open_port(CS['comport'], CS['comportSpeed'])

    @staticmethod
    @_handle_kkt_errors
    def close_port(*args, **kwargs):
        real_kkt.close_port()
        return {}

    @staticmethod
    @_handle_kkt_errors
    def open_shift(*args, **kwargs):
        return real_kkt.open_shift(*args)

    @staticmethod
    @_handle_kkt_errors
    def close_shift(*args, **kwargs):
        real_kkt.close_shift_pin_pad(*args)
        return real_kkt.close_shift(*args)

    @staticmethod
    @_handle_kkt_errors
    def force_close_shift(*args, **kwargs):
        return real_kkt.force_close_shift()

    @staticmethod
    @_handle_kkt_errors
    def handle_order(*args, **kwargs):
        cashier = kwargs['cashier_name']
        p_type = kwargs['payment_type']
        d_type = kwargs['document_type']
        wares = kwargs['wares']
        money_given = kwargs.get('amount_entered', 0)
        pay_link = kwargs.get('pay_link', '')
        pref = kwargs.get('order_prefix', '')
        return real_kkt.new_transaction(
            cashier=cashier, payment_type=p_type, doc_type=d_type,
            wares=copy.copy(wares), amount=money_given, rrn=pay_link,
            order_prefix=pref
        )

    @staticmethod
    @_handle_kkt_errors
    def insert_remove_operation(*args, **kwargs):
        return real_kkt.handler_cash_drawer(*args)

    @staticmethod
    @_handle_kkt_errors
    def set_zero_cash_drawer(*args, **kwargs):
        return real_kkt.set_zero_cash_drawer(*args)

    @staticmethod
    @_handle_kkt_errors
    def get_info(*args, **kwargs):
        return real_kkt.kkt_info()
