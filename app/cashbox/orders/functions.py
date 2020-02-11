from dateutil import parser
from app.kkt_device.decorators import validate_kkt_state, kkt_comport_activation, \
    check_for_opened_shift_in_fiscal
from app.kkt_device.models import KKTDevice
from app.cashbox.main_cashbox.models import Cashbox
from app.exceptions import CashboxException
from app.enums import DocumentTypes, PaymentChoices
from app.helpers import generate_internal_order_id, get_cheque_number, round_half_down
from .schemas import PaygateOrderSchema

from pprint import pprint as pp


@kkt_comport_activation()
@validate_kkt_state()
@check_for_opened_shift_in_fiscal()
async def create_order(*args, **kwargs):
    cashbox = Cashbox.box()
    if not cashbox.cash_character:
        msg = 'Символ кассы отсутствует. Зарегистрируйте'
        raise CashboxException(data=msg)

    req_data, kkt_info = kwargs['valid_schema_data'], kwargs['opened_port_info']
    cashier_name = req_data['cashier_name']
    cashier_id = req_data['cashier_id']
    payment_type = req_data['payment_type']
    document_type = DocumentTypes.PAYMENT.value
    amount_entered = req_data['amount_entered']
    wares = req_data['wares']
    character = cashbox.cash_character

    kkt_kwargs = {
        'cashier_name': cashier_name,
        'payment_type': payment_type,
        'document_type': document_type,
        'order_prefix': f'{character}-',
        'amount_entered': amount_entered,
        'wares': wares
    }

    created_order = KKTDevice.handle_order(**kkt_kwargs)
    data_to_db_and_paygate = {
        'cashier_name': cashier_name,
        'cashier_id': cashier_id,
        'clientOrderID': generate_internal_order_id(),
        'amount': round_half_down(created_order['transaction_sum'], 2),
        'creation_date': created_order['datetime'],
        'cashID': cashbox.cash_id,
        'checkNumber': get_cheque_number(created_order['check_number']),
        'doc_number': created_order['doc_number'],
        'cardHolder': created_order.get('cardholder_name', ''),
        'pan': created_order.get('pan_card', ''),
        'payLink': created_order.get('rrn', ''),
        'payType': payment_type,
        'payd': 1,
        # 'wares': wares
    }
    order = PaygateOrderSchema().load(data_to_db_and_paygate).data
    order.save()


async def return_order():
    pass