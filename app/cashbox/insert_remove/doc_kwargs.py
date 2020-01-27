from starlette.status import HTTP_200_OK
from .schemas import ResponseCashIn, ResponseCashOut

doc_cash_in = {
    'response_model': ResponseCashIn,
    'description': 'Операция внесения',
    'summary': 'Операция внесения',
    'response_description': 'Внесение успешно',
    'status_code': HTTP_200_OK,
}
doc_cash_out = {
    'response_model': ResponseCashOut,
    'description': 'Операция изъятия',
    'summary': 'Операция изъятия',
    'response_description': 'Изъятие успешно',
    'status_code': HTTP_200_OK,
}