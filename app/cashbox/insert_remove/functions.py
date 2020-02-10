from app.kkt_device.decorators import kkt_comport_activation, validate_kkt_state, \
    check_for_opened_shift_in_fiscal
from .models import CashOperation
from .schemas import DBPaygateCashInSchema, DBPaygateCashOutSchema
from app.enums import DocumentTypes, PaygateURLs
from app.kkt_device.models import KKTDevice
from app.cashbox.main_cashbox.models import Cashbox


@kkt_comport_activation()
@validate_kkt_state()
@check_for_opened_shift_in_fiscal()
async def handle_insert(*args, **kwargs):
    await handle_money_transfer(
        *args, **kwargs,
        document_type=DocumentTypes.INSERT,
        paygate_model=DBPaygateCashInSchema,
        paygate_url=PaygateURLs.insert_cash
    )
    return {}


@kkt_comport_activation()
@validate_kkt_state()
@check_for_opened_shift_in_fiscal()
async def handle_remove(*args, **kwargs):
    await handle_money_transfer(
        *args, **kwargs,
        document_type=DocumentTypes.REMOVE,
        paygate_model=DBPaygateCashOutSchema,
        paygate_url=PaygateURLs.remove_cash
    )
    return {}


async def handle_money_transfer(*args, **kwargs):
    req_data, kkt_info = kwargs['valid_schema_data'], kwargs['opened_port_info']
    cashbox = Cashbox.box()
    cashier_name = req_data['cashier_name']
    cashier_id = req_data['cashier_id']
    amount = req_data['amount']
    pennies = int(amount * 100)
    doc_type = kwargs['document_type']
    paygate_model = kwargs['paygate_model']
    paygate_url = kwargs['paygate_url']

    kkt_result = KKTDevice.insert_remove_operation(cashier_name, pennies, doc_type)

    data_to_db = {
        'cashier_id': cashier_id, 'cashier_name': cashier_name,
        'amount': amount, 'document_type': doc_type}
    operation = CashOperation().map_to_fields({**kkt_info, **kkt_result, **data_to_db})
    cashbox.add_cash_operation_to_shift(operation)
    cashbox.update_shift_money_counter(doc_type, amount)
    data_to_paygate = paygate_model().dump(operation.paygate_data).data
    data_to_paygate.update({'url': paygate_url})
    cashbox.save_paygate_data_for_send(data_to_paygate)

