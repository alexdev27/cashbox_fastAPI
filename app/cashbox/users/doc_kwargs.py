from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from .schemas import ResponseCreateUser, ResponseGetUser

doc_get_user = {
    'description': 'Получение информации о пользователе',
    'summary': 'Получение информации о пользователе',
    'response_description': 'Информация',
    'status_code': HTTP_200_OK,
    'response_model': ResponseGetUser
}

doc_create_user = {
    'description': 'Создание пользователя',
    'summary': 'Создание пользователя',
    'response_description': 'Пользователь создан',
    'status_code': HTTP_200_OK,
    'response_model': ResponseCreateUser
}

doc_update_user = {
    'description': 'Обновление данных пользователя',
    'summary': 'Обновление данных пользователя',
    'response_description': 'Пользователь обновлен',
    'status_code': HTTP_204_NO_CONTENT,
}

doc_delete_user = {
    'description': 'Удаление пользователя',
    'summary': 'Удаление пользователя',
    'response_description': 'Пользователь удален',
    'status_code': HTTP_204_NO_CONTENT
}
