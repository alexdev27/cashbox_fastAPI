from starlette.status import HTTP_200_OK
from .schemas import ResponseOpenShift


doc_open_shift = {
    'response_model': ResponseOpenShift,
    'description': 'Операция открытия смены',
    'summary': 'Операция открытия смены',
    'response_description': 'Открытие смены прошло успешно',
    'status_code': HTTP_200_OK,
}
