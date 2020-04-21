import abc
import copy
from functools import wraps

from app.helpers import round_half_down
from config import CASH_SETTINGS as CS
import cashbox as real_kkt
from app.exceptions import CashboxException


class IKKTDevice(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'open_comport') and
                callable(subclass.open_comport) and
                hasattr(subclass, 'close_port') and
                callable(subclass.close_port) and
                hasattr(subclass, 'open_shift') and
                callable(subclass.open_shift) and
                hasattr(subclass, 'close_shift') and
                callable(subclass.close_shift) and
                hasattr(subclass, 'handle_order') and
                callable(subclass.handle_order) and
                hasattr(subclass, 'insert_remove_operation') and
                callable(subclass.insert_remove_operation) and
                hasattr(subclass, 'get_info') and
                callable(subclass.get_info) and
                hasattr(subclass, 'startup') and
                callable(subclass.startup)
                or NotImplemented)

    @abc.abstractmethod
    def startup(*args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def open_comport(*args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def close_port(*args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def open_shift(*args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def close_shift(*args, **kwargs):
        raise NotImplementedError

    # @abc.abstractmethod
    # def force_close_shift(*args, **kwargs):
    #     pass

    @abc.abstractmethod
    def handle_order(*args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def insert_remove_operation(*args, **kwargs):
        raise NotImplementedError

    # @abc.abstractmethod
    # def set_zero_cash_drawer(*args, **kwargs):
    #     pass

    @abc.abstractmethod
    def get_info(*args, **kwargs):
        raise NotImplementedError


def _handle_kkt_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result.get('error'):
                msg = f'Ошибка при открытии порта: {result}'
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


class Pirit2f(IKKTDevice):

    def startup(*args, **kwargs):
        pass

    # def register_fiscal_cashier(*args, **kwargs):
    #     pass

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
        c_name = args[1]
        return real_kkt.open_shift(c_name)

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
        result = real_kkt.new_transaction(
            cashier=cashier, payment_type=p_type, doc_type=d_type,
            wares=copy.copy(wares), amount=money_given, rrn=pay_link,
            order_prefix=pref
        )

        info = {}
        transaction_sum = round_half_down(result['transaction_sum'] - result['discount_sum'], 2)
        info['cashier_name'] = result['cashier']
        info['datetime'] = result['datetime']
        info['doc_number'] = result['doc_number']
        info['total_without_discount'] = transaction_sum

        info['transaction_sum'] = transaction_sum
        info['check_number'] = result['check_number']
        info['order_num'] = int(str(result['check_number']).rsplit('.', maxsplit=1)[-1])
        info['rrn'] = result.get('rrn', '')
        info['pan_card'] = result.get('pan_card', '')
        info['cardholder_name'] = result.get('cardholder_name', '')
        return info

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
