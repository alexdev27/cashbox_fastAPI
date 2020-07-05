from starlette.status import HTTP_200_OK
from .schemas import Token

doc_login = {
    'response_model': Token,
    'description': 'Вход пользователя в систему (генерация jwt-токена)',
    'summary': 'Вход пользователя в систему (генерация jwt-токена)',
    'response_description': 'Токен',
    'status_code': HTTP_200_OK,
}
