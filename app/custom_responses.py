from fastapi.openapi.constants import REF_PREFIX
from .schemas import CashboxExceptionSchema

# Кастомный респонс для 400 ошибки
response_400 = {
    '400': {
        'description': 'internal Application Error aka Bad Request',
        'content': {
            'application/json': {
                'schema': {
                    '$ref': f'{REF_PREFIX}{CashboxExceptionSchema.schema()["title"]}'
                }
            }
        }
    }
}
