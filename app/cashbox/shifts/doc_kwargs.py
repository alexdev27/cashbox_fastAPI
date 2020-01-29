from starlette.status import HTTP_200_OK
from .schemas import ResponseCloseShift, ResponseOpenShift, ResponseCurrentShiftInfo


doc_close_shift = {
    'response_model': ResponseCloseShift,
    'description': 'Операция закрытия смены',
    'summary': 'Операция закрытия смены',
    'response_description': 'Закрытие смены прошло успешно',
    'status_code': HTTP_200_OK,
}

doc_open_shift = {
    'response_model': ResponseOpenShift,
    'description': 'Операция открытия смены',
    'summary': 'Операция открытия смены',
    'response_description': 'Открытие смены прошло успешно',
    'status_code': HTTP_200_OK,
}

doc_current_shift_info = {
    'response_model': ResponseCurrentShiftInfo,
    'description': 'Получение информации о смене',
    'summary': 'Получение информации о смене',
    'response_description': 'Информация о смене',
    'status_code': HTTP_200_OK,
}