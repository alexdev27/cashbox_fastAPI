from starlette.status import HTTP_200_OK
from .schemas import ResponseCreateOrder

doc_create_order = {
    'response_model': ResponseCreateOrder,
    'description': 'Операция создания заказа (совершения оплаты)',
    'summary': 'Операция создания заказа (совершения оплаты)',
    'response_description': 'Создание заказа (совершение оплаты) прошло успешно',
    'status_code': HTTP_200_OK,
}
