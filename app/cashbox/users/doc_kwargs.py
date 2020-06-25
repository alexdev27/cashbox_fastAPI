from starlette.status import HTTP_201_CREATED


doc_create_user = {
    'description': 'Создание пользователя',
    'summary': 'Создание пользователя',
    'response_description': 'Пользователь создан',
    'status_code': HTTP_201_CREATED,
}
