from starlette.status import HTTP_200_OK
from .schemas import ResponseCreateOrder, ResponseReturnOrder

doc_create_order = {
    'response_model': ResponseCreateOrder,
    'description': 'Операция создания заказа (совершения оплаты)',
    'summary': 'Операция создания заказа (совершения оплаты)',
    'response_description': 'Создание заказа (совершение оплаты) прошло успешно',
    'status_code': HTTP_200_OK,
}

doc_return_order = {
    'response_model': ResponseReturnOrder,
    'description': 'Операция возврата денег за заказ',
    'summary': 'Операция возврата денег за заказ',
    'response_description': 'Операция возврата денег за заказ прошла успешно',
    'status_code': HTTP_200_OK
}
