from app.kkt_device.decorators import kkt_comport_activation, validate_kkt_state, \
    check_for_opened_shift_in_fiscal, check_for_closed_shift_in_fiscal
from app.cashbox.main_cashbox.models import Cashbox
from app import KKTDevice
from app.helpers import get_WIN_UUID
from app.enums import PaygateURLs
from .schemas import OpenShiftSchema, CloseShiftSchema
from app.helpers import round_half_down
from app.logging import logging_decorator
# from pprint import pprint as pp


@logging_decorator('shift_logs.log', 'shift_logger', 'OPEN SHIFT')
@kkt_comport_activation()
@validate_kkt_state()
@check_for_closed_shift_in_fiscal()
async def open_new_shift(*args, **kwargs):
    cashbox = Cashbox.box()
    req_data, kkt_info = kwargs['valid_schema_data'], kwargs['opened_port_info']
    cashier_name, cashier_id = req_data['cashier_name'], req_data['cashier_id']
    open_shift_data = KKTDevice.open_shift(cashbox.cash_number, cashier_name)
    data_to_db = {
        'cashier_name': cashier_name, 'cashier_id': cashier_id,
        'shop_number': cashbox.shop, 'project_number': cashbox.project_number,
        'system_id': get_WIN_UUID(), 'cash_number': cashbox.cash_number,
        'cash_name': cashbox.cash_name
    }
    shift, errs = OpenShiftSchema().load({**kkt_info, **open_shift_data, **data_to_db})
    cashbox.set_current_shift(shift)
    data_to_paygate = OpenShiftSchema.get_data_for_paygate(shift)
    data_to_paygate.update({'url': PaygateURLs.open_shift})
    cashbox.save_paygate_data_for_send(data_to_paygate)
    return {}


@logging_decorator('shift_logs.log', 'shift_logger', 'CLOSE SHIFT')
@kkt_comport_activation()
@validate_kkt_state(skip_shift_check=True)
@check_for_opened_shift_in_fiscal()
async def close_current_shift(*args, **kwargs):
    cashbox: Cashbox = Cashbox.box()
    req_data, kkt_info = kwargs['valid_schema_data'], kwargs['opened_port_info']
    cashier_name, cashier_id = req_data['cashier_name'], req_data['cashier_id']
    close_shift_data = KKTDevice.close_shift(cashier_name)
    data_to_db = {'cashier_name': cashier_name, 'cashier_id': cashier_id}
    closed_shift, errs = CloseShiftSchema().load({**kkt_info, **close_shift_data, **data_to_db})
    cashbox.close_shift(closed_shift)
    data_to_paygate = CloseShiftSchema.get_data_for_paygate(closed_shift)
    data_to_paygate.update({'url': PaygateURLs.close_shift})
    cashbox.save_paygate_data_for_send(data_to_paygate)
    return {}


@kkt_comport_activation()
@validate_kkt_state()
@check_for_opened_shift_in_fiscal()
async def get_shift_info(*args, **kwargs):
    result = kwargs['opened_port_info']
    current_shift = Cashbox.box().current_opened_shift
    shift_info = {
        'shift_open_time': str(current_shift.creation_date).replace('T', ' '),
        'total_money_in_cashbox': round_half_down(result['cash_balance'] / 100, 2),
        'shift_number': current_shift.shiftNumber,
        'shift_total_inserted': current_shift.total_inserted_money_in_shift,
        'shift_total_removed': current_shift.total_removed_money_in_shift,
        'shift_total_sales': current_shift.total_sales_in_shift,
        'shift_total_returns': current_shift.total_returns_in_shift,
        'start_shift_money': current_shift.start_shift_money
    }
    return shift_info
