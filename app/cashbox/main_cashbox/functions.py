from app.kkt_device.decorators import kkt_comport_activation, validate_kkt_state
from config import CASH_SETTINGS as CS
from app.exceptions import CashboxException
from app.helpers import request_to_paygate, get_WIN_UUID
from .models import Cashbox
from .schemas import RequestRegisterCashboxCharacter
from app.enums import PaygateURLs
from dateutil import parser


@kkt_comport_activation()
async def init_cashbox(*args, **kwargs):
    """ Первоначальная инициализация кассы. """

    result = kwargs['opened_port_info']
    shop_num, cash_id, sys_id = (CS['shopNumber'], result.get('fn_number'), get_WIN_UUID())

    if not cash_id:
        err = 'Ошибка: Не удалось получить из ККТ fn_number'
        raise CashboxException(data=err)

    # # proj - номер системы, с которой происходит запрос
    obj = {'shop': shop_num, 'cashID': cash_id, 'systemID': sys_id, 'proj': 1}
    print('TO paygate -> ', obj)
    paygate_content = await request_to_paygate(PaygateURLs.register_cash, 'post', obj)

    cash_num = paygate_content.get('cashNumber')

    cashbox = Cashbox.objects(cash_id=cash_id, cash_number=cash_num).first()
    Cashbox.set_all_inactive()
    if cashbox:
        cashbox.reload()
        cashbox.activation_date = parser.parse(result['datetime'])
        cashbox.is_active = True
        cashbox.save().reload()
        print('is cashbox active right now? ', cashbox.is_active)
    else:
        cashbox = Cashbox()
        cashbox.creation_date = parser.parse(result['datetime'])
        cashbox.shop = CS['shopNumber']
        cashbox.cash_number = cash_num
        cashbox.cash_name = CS['cashName']
        cashbox.cash_id = cash_id
        cashbox.project_number = obj['proj']
        cashbox.save().reload()


# @kkt_comport_activation()
async def register_cashbox_character(*args, **kwargs):
    req_data = kwargs['valid_schema_data']
    char = req_data['character']
    cashbox = Cashbox.box()
    cashbox.cash_character = char
    cashbox.save()
    return {'character': char}


async def get_sys_id():
    return {'device_id': get_WIN_UUID()}