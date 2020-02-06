from copy import deepcopy
from app.cashbox.main_cashbox.models import DataToPayGate
from app.helpers import request_to_paygate
from app.exceptions import CashboxException
from app import celery
import asyncio


@celery.on_after_configure.connect
def setup_periodic(sender, **kwargs):
    sender.add_periodic_task(10, task_.s(), name='data_to_paygate')


async def try_send_to_paygate():
    copy_of_data = deepcopy(DataToPayGate.objects())
    for payment_data in copy_of_data:
        data = payment_data.data
        print(data)
        try:
            await request_to_paygate(data['url'], 'POST', data)
        except CashboxException as exc:
            msg = f' <<< CashboxException inside Celery task! >>>  {exc.data}'
            print(msg)
            return
        DataToPayGate.objects.get(id=payment_data.id).delete()


@celery.task(ignore_results=True)
def task_():
    asyncio.run(try_send_to_paygate())
