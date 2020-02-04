from app.kkt_device.decorators import kkt_comport_activation, validate_kkt_state, \
    check_for_opened_shift_in_fiscal, check_for_closed_shift_in_fiscal
from app.cashbox.main_cashbox.models import Cashbox
from app.kkt_device.models import KKTDevice


@kkt_comport_activation()
@validate_kkt_state()
@check_for_closed_shift_in_fiscal()
async def open_new_shift(*args, **kwargs):
    cashbox = Cashbox.box()
    req_data = kwargs['valid_schema_data']
    kkt_info = kwargs['opened_port_info']
    cashier_name, cashier_id = req_data['cashier_name'], req_data['cashier_id']
    # print(args, kwargs)
    open_shift_data = KKTDevice.open_shift(cashier_name)
    print('kkt_info -> ', kkt_info)
    print('open_shift_info -> ', open_shift_data)

    return



def close_current_shift(*args, **kwargs):
    pass


def get_shift_info(*args, **kwargs):
    pass
