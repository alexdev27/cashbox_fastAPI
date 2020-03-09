from starlette.status import HTTP_200_OK
from .schemas import ResponseRegisterCashboxCharacter, \
    ResponseGetSystemID


doc_register_character = {
    'response_model': ResponseRegisterCashboxCharacter,
    'description': 'Регистрация символа кассы',
    'summary': 'Регистрация символа кассы',
    'response_description': 'Символ зарегистрирован успешно',
    'status_code': HTTP_200_OK,
}

doc_get_sys_id = {
    'response_model': ResponseGetSystemID,
    'description': 'Получение идентификатора устройства',
    'summary': 'Получение идентификатора устройства',
    'response_description': 'Идентификатор устройства',
    'status_code': HTTP_200_OK,
}
#
# doc_register_fiscal_cashier = {
#     'response_model': ResponseRegisterFiscalCashier,
#     'description': 'Регистрация кассира в фисальном регистраторе',
#     'summary': 'Регистрация кассира в фисальном регистраторе',
#     'response_description': 'Зарегистрирован успешно',
#     'status_code': HTTP_200_OK,
# }