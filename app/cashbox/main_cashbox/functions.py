from app.kkt_device.decorators import kkt_comport_activation
from config import CASH_SETTINGS as CS
from app.exceptions import CashboxException
from app.helpers import request_to_paygate, get_WIN_UUID
from .models import Cashbox
from app.enums import PaygateURLs


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
    paygate_content = await request_to_paygate(PaygateURLs.register_cash, 'post', obj)

    cash_num = paygate_content.get('cashNumber')

    cashbox = Cashbox.objects(cash_id=cash_id, cash_number=cash_num).first()
    Cashbox.set_all_inactive()
    if cashbox:
        cashbox.reload()
        cashbox.is_active = True
        cashbox.save().reload()
        print('is cashbox active right now? ', cashbox.is_active)
    else:
        cashbox = Cashbox(shop=CS['shopNumber'], cash_number=cash_num,
                          cash_name=CS['cashName'], cash_id=cash_id)
        cashbox.save().reload()
