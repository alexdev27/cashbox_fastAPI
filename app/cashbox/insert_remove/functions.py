from app.kkt_device.decorators import kkt_comport_activation
from typing import Dict


@kkt_comport_activation()
async def handle_insert(*args, **kwargs):
    print('kwargs -> ', kwargs)
    return {'msg': 'Success', 'amount': 342}


@kkt_comport_activation()
def handle_remove(*args, **kwargs) -> Dict:
    pass
