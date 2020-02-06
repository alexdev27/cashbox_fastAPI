from functools import wraps
from app.exceptions import CashboxException
from app.kkt_device.models import KKTDevice
from .constants import ERR_DB_SHIFT_OPENED_BUT_NOT_IN_FISCAL, ERR_FISCAL_SHIFT_OPENED_BUT_NOT_IN_DB, \
    ERR_SHIFT_NUMBER_NOT_SYNCED, ERR_IF_FISCAL_ID_NOT_SYNCED
from app.cashbox.main_cashbox.models import Cashbox
from pprint import pprint as pp


def kkt_comport_activation():
    """ Активация COM порта """
    def open_comport(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            opened_port = KKTDevice.open_comport()
            kwargs.update({'opened_port_info': opened_port})
            result = await func(*args, **kwargs)
            KKTDevice.close_port()
            return result
        return wrapper
    return open_comport


def _is_fiscal_shift_opened(kwargs):
    return kwargs['opened_port_info']['is_open_shift']


def check_for_opened_shift_in_fiscal(err_if_opened=False):
    def _check_for_opened_shift_in_fiscal(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            msg = 'Смена в фискальном регистраторе'
            if _is_fiscal_shift_opened(kwargs):
                if err_if_opened:
                    raise CashboxException(data=msg+' уже открыта')
                else:
                    return await func(*args, **kwargs)
            else:
                raise CashboxException(data=msg+' еще не открыта')
        return wrapper
    return _check_for_opened_shift_in_fiscal


def check_for_closed_shift_in_fiscal(err_if_closed=False):
    def _check_for_closed_shift_in_fiscal(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            msg = 'Смена в фискальном регистраторе'
            if not _is_fiscal_shift_opened(kwargs):
                if err_if_closed:
                    raise CashboxException(data=msg+' уже закрыта')
                else:
                    return await func(*args, **kwargs)
            else:
                raise CashboxException(data=' еще открыта')
        return wrapper
    return _check_for_closed_shift_in_fiscal


def validate_kkt_state(skip_shift_check=False):
    def _validate_kkt_state(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cb = Cashbox.box()
            is_opened_fiscal_shift = kwargs['opened_port_info']['is_open_shift']
            current_fiscal_shift_number = kwargs['opened_port_info']['shift_number']
            actual_fiscal_device_number = kwargs['opened_port_info']['fn_number']
            current_fiscal_device_number_in_db = cb.cash_id
            current_shift_in_db = cb.current_opened_shift
            # current_shift_number = cb.current_opened_shift.paygate_data.shiftNumber

            # print('shiftnumbers ', current_shift_number, current_fiscal_shift_number)

            if current_fiscal_device_number_in_db != actual_fiscal_device_number:
                raise CashboxException(data=ERR_IF_FISCAL_ID_NOT_SYNCED)
            if skip_shift_check:
                return await func(*args, **kwargs)
            if is_opened_fiscal_shift:
                if current_shift_in_db:
                    if current_shift_in_db.paygate_data.shiftNumber != current_fiscal_shift_number:
                        print(current_shift_in_db.paygate_data.shiftNumber)
                        print(current_fiscal_shift_number)
                        raise CashboxException(data=ERR_SHIFT_NUMBER_NOT_SYNCED)
                else:
                    # TODO: Подумать о экстренном закрытии смены на paygate сервисе вместе с фискальиком
                    KKTDevice.force_close_shift()
                    msg = f'{ERR_FISCAL_SHIFT_OPENED_BUT_NOT_IN_DB}. ' \
                          f'Смена закрыта принудительно. ' \
                          f'Теперь откройте смену'
                    raise CashboxException(data=msg)
            else:
                if current_shift_in_db:
                    cb.current_opened_shift = None
                    cb.save()
                    raise CashboxException(data=ERR_DB_SHIFT_OPENED_BUT_NOT_IN_FISCAL)
            return await func(*args, **kwargs)
        return wrapper
    return _validate_kkt_state
