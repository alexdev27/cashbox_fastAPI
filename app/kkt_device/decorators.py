from functools import wraps


def kkt_comport_activation():
    """ Активация COM порта """
    def open_comport(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pass
            # opened_port = kkt_device.open_port(cs['comport'], cs['comportSpeed'])
            # if opened_port['error']:
            #     msg = f'Ошибка при открытии порта: {opened_port["message"]}'
            #     print(msg)
            #     return return_fail_info(msg=msg)
            #
            # if opened_port['status_printer_error_code'] > 0:
            #     code = opened_port['status_printer_error_code']
            #     err_msg = opened_port['status_printer_message']
            #     msg = f'Ошибка принтера: Код: {code} Сообщение: {err_msg}'
            #     print(msg)
            #     return return_fail_info(msg=msg)
            # kwargs.update({'opened_port_info': opened_port})
            # для тестирования
            # from app.cash_reports.models import FakeFiscal
            # fiscal_number = kwargs['opened_port_info']['fn_number']
            # ff = FakeFiscal.objects().first()
            # if ff:
            #     fiscal_number += ff.fake_num
            #     kwargs['opened_port_info'].update({'fn_number': fiscal_number})

            # result = func(*args, **kwargs)
            # kkt_device.close_port()
            # return result
        return wrapper
    return open_comport
