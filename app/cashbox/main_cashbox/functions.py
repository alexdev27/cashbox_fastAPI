from app.enums import PaygateURLs
from app.exceptions import CashboxException
from app.helpers import request_to_paygate
from app.kkt_device.decorators import kkt_comport_activation
from app.logging import logging_decorator
from config import CASH_SETTINGS as CS
from .models import Cashbox, System


@kkt_comport_activation()
async def init_cashbox(*args, **kwargs):
    """ Первоначальная инициализация кассы. """

    result = kwargs['opened_port_info']
    shop_num, cash_id, sys_id = (CS['shopNumber'], result.get('fn_number'), System.get_sys_id())

    if not cash_id:
        err = 'Ошибка: Не удалось получить из ККТ fn_number'
        raise CashboxException(data=err)

    # # proj - номер системы, с которой происходит запрос
    obj = {'shop': shop_num, 'cashID': cash_id, 'systemID': sys_id, 'proj': 1}
    print('request to paygate -> ', obj)
    paygate_content = await request_to_paygate(CS['paygateAddress'] + PaygateURLs.register_cash, 'post', obj)
    print('response from paygate', paygate_content)
    cash_num = paygate_content.get('cashNumber')

    cashbox = Cashbox.objects(cash_id=cash_id, cash_number=cash_num).first()
    Cashbox.set_all_inactive()
    if cashbox:
        cashbox.reload()
        cashbox.activation_date = result['datetime']
        cashbox.is_active = True
        cashbox.save().reload()
        print('is cashbox active right now? ', cashbox.is_active)
    else:
        cashbox = Cashbox()
        cashbox.creation_date = result['datetime']
        cashbox.shop = CS['shopNumber']
        cashbox.cash_number = cash_num
        cashbox.cash_name = CS['cashName']
        cashbox.cash_id = cash_id
        cashbox.project_number = obj['proj']
        cashbox.save().reload()


@logging_decorator('main.log', 'main_module_logger', 'REGISTER CHARACTER')
# @kkt_comport_activation()
async def register_cashbox_character(*args, **kwargs):
    req_data = kwargs['valid_schema_data']
    char = req_data['character']
    cashbox = Cashbox.box()
    cashbox.cash_character = char
    cashbox.save()
    return {'character': char}


# @kkt_comport_activation()
# async def register_fiscal_cashier(*args, **kwargs):
#     req_data = kwargs['valid_schema_data']
#     KKTDevice.register_fiscal_cashier(**kwargs)
#     return {}
#


@logging_decorator('main.log', 'main_module_logger', 'GET SYS ID')
async def get_sys_id():
    return {'device_id': System.get_sys_id()}
