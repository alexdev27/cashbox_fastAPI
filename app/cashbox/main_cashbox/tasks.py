from copy import deepcopy
from app.cashbox.main_cashbox.models import DataToPayGate
from app.helpers import request_to_paygate
from app.exceptions import CashboxException
from app import celery
from config import CASH_SETTINGS
import asyncio


from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.on_after_configure.connect
def setup_periodic(sender, **kwargs):
    sender.add_periodic_task(20, check_cashbox_info.s(), name='data_to_paygate')


async def try_send_to_paygate():
    copy_of_data = deepcopy(DataToPayGate.objects())
    for payment_data in copy_of_data:
        data = payment_data.data
        data['url'] = CASH_SETTINGS['paygateAddress'] + data['url']
        print('send to ', data['url'])
        try:
            await request_to_paygate(data['url'], 'POST', data)
        except CashboxException as exc:
            msg = f' <<< CashboxException inside Celery task! >>>  {exc.data}'
            print(msg)
            return
        DataToPayGate.objects.get(id=payment_data.id).delete()


@celery.task(ignore_results=True, name='check_unsent_data')
def check_cashbox_info():
    asyncio.run(try_send_to_paygate())
