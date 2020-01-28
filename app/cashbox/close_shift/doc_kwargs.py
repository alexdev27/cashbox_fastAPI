from starlette.status import HTTP_200_OK
from .schemas import ResponseCloseShift


doc_close_shift = {
    'response_model': ResponseCloseShift,
    'description': 'Операция закрытия смены',
    'summary': 'Операция закрытия смены',
    'response_description': 'Закрытие смены прошло успешно',
    'status_code': HTTP_200_OK,
}