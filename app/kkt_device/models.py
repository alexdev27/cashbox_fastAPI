import abc
import copy
from functools import wraps

from app.logging import get_logger
from app.helpers import round_half_down
from app.enums import DocumentTypes
from config import CASH_SETTINGS as CS
import cashbox as real_kkt
from app.exceptions import CashboxException

DEFAULT_CASHIER_NAME = 'Mr. Printer'



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
                _msg = f'{result.get("description_error", "")} {result.get("message", "")}'

                raise CashboxException(data=_msg, to_logging=msg)
                # raise CashboxException(data=msg)
            if result.get('status_printer_error_code'):
                if result['status_printer_error_code'] > 0:
                    code = result['status_printer_error_code']
                    err_msg = result['status_printer_message']
                    msg = f'Ошибка фискального регистратора: ' \
                          f'Код: {code} Сообщение: {err_msg}'
                    raise CashboxException(data=msg, to_logging=f'Ошибка фискальника {result}')
            return result

        except CashboxException as c_exc:
            msg = f'Фискальный регистратор не смог ' \
                  f'выполнить функцию ({func.__name__}) ' \
                  f'Тип ошибки: {c_exc.__class__.__name__} ' \
                  f'Описание: {str(c_exc)}'
            to_log = c_exc.to_logging if c_exc.to_logging else msg
            raise CashboxException(data=msg, to_logging=to_log)
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
        info = real_kkt.close_shift(*args)

        arcus_logger = get_logger('arcus_logs.txt', 'arcus_logger')

        arcus_logger.info(f'=== Начало исполнения функции в пакете {__file__}'
                          f' - {real_kkt.close_shift_pin_pad.__name__}')

        try:
            arcus_info = real_kkt.close_shift_pin_pad(*args)
            if arcus_info['error']:
                raise Exception(arcus_info)
            arcus_logger.info(f'=== Функция {real_kkt.close_shift_pin_pad.__name__} завершилась без ошибок')
        except Exception as e:
            arcus_logger.error(f'\t====== Error ======\n'
                               f'\tОшибка при исполнении функции {real_kkt.close_shift_pin_pad.__name__}.\n'
                               f'\tДетали ошибки: {str(e)}')

        return info

    @staticmethod
    @_handle_kkt_errors
    def force_close_shift(*args, **kwargs):
        return real_kkt.force_close_shift()

    @staticmethod
    @_handle_kkt_errors
    def handle_order(*args, **kwargs):
        cashier = kwargs['cashier_name'] or DEFAULT_CASHIER_NAME
        p_type = kwargs['payment_type']
        d_type = kwargs['document_type']
        order_number = kwargs.get('order_number', 0)
        wares = kwargs['wares']
        money_given = kwargs.get('amount_entered', 0)
        pay_link = kwargs.get('pay_link', '')
        pref = kwargs.get('order_prefix', '')
        order_number += 1
        print('orderr number -> ', order_number, 'pay_link ', pay_link)
        text = f"\n\n\n--------------------------------------------\n" \
               f"(font-style=BIG_BOLD)     НОМЕР ЗАКАЗА: (font-style=BIG_BOLD){pref}{order_number}" \
               f"\n --------------------------------------------\n\n"
        result = real_kkt.new_transaction(
            cashier=cashier, payment_type=p_type, doc_type=d_type,
            wares=copy.copy(wares), amount=money_given, rrn=pay_link,
            # order_prefix=pref,
            print_strings=text if d_type == DocumentTypes.PAYMENT else ''
        )

        if result['error']:
            msg = 'Терминал безналичной оплаты вернул ошибку во время транзакции'
            raise CashboxException(data=msg, to_logging=msg + f'\nИнформация с аркуса: {result}')

        from pprint import pprint as pp
        print('FROM FISKALNIK')
        pp(result)

        info = {}
        transaction_sum = round_half_down(result['transaction_sum'] - result['discount_sum'], 2)
        info['cashier_name'] = result['cashier']
        info['datetime'] = result['datetime']
        info['doc_number'] = result['doc_number']
        # При наличном платеже с пирита приходит transaction_sum без округления в меньшую сторону,
        # и пока можно оставить строчку ниже без изменений
        info['total_without_discount'] = round_half_down(result['transaction_sum'], 2)

        info['transaction_sum'] = transaction_sum
        # info['check_number'] = result['check_number']
        info['check_number'] = str(int(str(result['check_number']).rsplit('.', maxsplit=1)[-1]))
        info['order_num'] = order_number
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
