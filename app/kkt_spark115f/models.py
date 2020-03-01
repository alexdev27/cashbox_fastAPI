from functools import wraps
from .err_codes import check_for_err_code
from .enums import KKTInfoEnum
from comtypes.client import CreateObject
from comtypes.gen._445B09C3_EF00_47B4_9DB0_68DDD7AA9FF1_0_1_0 import FPSpark, IFPSpark

from app.kkt_device.models import IKKTDevice
from app.exceptions import CashboxException


def _handle_kkt_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            msg = f'Фискальный регистратор не смог ' \
                  f'выполнить функцию ({func.__name__}) ' \
                  f'Тип ошибки: {exc.__class__.__name__} ' \
                  f'Описание: {str(exc)}'
            raise CashboxException(data=msg)
    return wrapper
# TODO доделать надо

class Spark115f(IKKTDevice):

    kkt_object = CreateObject(FPSpark, None, None, IFPSpark)

    def open_comport(*args, **kwargs):
        status = Spark115f.kkt_object.InitDevice()
        Spark115fHelper.check_for_bad_code(Spark115f.kkt_object, status)

        # info =

    def close_port(*args, **kwargs):
        Spark115f.kkt_object.DeinitDevice()
        return {}

    def open_shift(*args, **kwargs):
        pass

    def close_shift(*args, **kwargs):
        pass

    def handle_order(*args, **kwargs):
        pass

    def insert_remove_operation(*args, **kwargs):
        pass

    def get_info(*args, **kwargs):
        pass


class Spark115fHelper:

    @staticmethod
    def check_for_bad_code(obj, code):
        if check_for_err_code(code):
            err_msg = obj.GetExtendedErrorComment(code)
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
            'cash_balance': h.get_current_cash_balance(obj)
        }

    @staticmethod
    def get_current_shift_number(obj):
        return int(str(obj.GetTextDeviceInfo(KKTInfoEnum.shift_number)).strip())

    @staticmethod
    def get_shift_open_close_time(obj):
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.shift_open_close_time)).strip()

    @staticmethod
    def get_current_time(obj):
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.current_time_and_date)).strip()

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
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.last_doc_number)).strip()

    @staticmethod
    def get_reg_number(obj):
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.reg_number)).strip()

    @staticmethod
    def get_factory_number(obj):
        return str(obj.GetTextDeviceInfo(KKTInfoEnum.factory_number)).strip()

    @staticmethod
    def is_open_shift(obj):
        status = int(obj.ChkShift())
        Spark115fHelper.check_for_bad_code(obj, status)

        if status == -2:
            return False
        elif status == -3:
            return True
