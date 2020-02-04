from app.kkt_device.decorators import kkt_comport_activation, validate_kkt_state
from app.cashbox.main_cashbox.models import Cashbox


@kkt_comport_activation()
@validate_kkt_state()
def open_new_shift(*args, **kwargs):
    cashbox = Cashbox.box()

    pass


def close_current_shift(*args, **kwargs):
    pass


def get_shift_info(*args, **kwargs):
    pass
