from starlette.status import HTTP_200_OK
from .schemas import ResponseCreateOrder, ResponseReturnOrder, ResponseRoundPrice, \
    ResponsePartialReturn

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

doc_round_price = {
    'response_model': ResponseRoundPrice,
    'description': 'Округление цены',
    'summary': 'Округление цены',
    'response_description': 'Округление цены прошло успешно',
    'status_code': HTTP_200_OK
}

doc_partial_return = {
    'response_model': ResponsePartialReturn,
    'description': 'Частичный возват',
    'summary': 'Частичный возврат',
    'response_description': 'Возврат прошел успешно',
    'status_code': HTTP_200_OK
}