from functools import wraps
from config import CASH_SETTINGS as CS
from app.exceptions import CashboxException
import cashbox as real_kkt
from typing import Callable


def kkt_comport_activation() -> Callable:
    """ Активация COM порта """
    def open_comport(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # pass
            opened_port = real_kkt.open_port(CS['comport'], CS['comportSpeed'])
            if opened_port['error']:
                msg = f'Ошибка при открытии порта: {opened_port["message"]}'
                print(msg)
                raise CashboxException(data=msg)

            if opened_port['status_printer_error_code'] > 0:
                code = opened_port['status_printer_error_code']
                err_msg = opened_port['status_printer_message']
                msg = f'Ошибка принтера: Код: {code} Сообщение: {err_msg}'
                print(msg)
                raise CashboxException(data=msg)
            kwargs.update({'opened_port_info': opened_port})
            # для тестирования
            # from app.cash_reports.models import FakeFiscal
            # fiscal_number = kwargs['opened_port_info']['fn_number']
            # ff = FakeFiscal.objects().first()
            # if ff:
            #     fiscal_number += ff.fake_num
            #     kwargs['opened_port_info'].update({'fn_number': fiscal_number})

            result = await func(*args, **kwargs)
            real_kkt.close_port()
            return result
        return wrapper
    return open_comport
