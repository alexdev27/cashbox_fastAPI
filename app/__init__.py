from fastapi import FastAPI, Query, Path

from fastapi.openapi.utils import get_openapi
from .schemas import CashboxExceptionSchema
from .cashbox.insert_remove.api_views import router as ir_router

app = FastAPI()

default_prefix = '/api'


def url_with_prefix(url: str = '') -> str:
    return f'{default_prefix}{url}'


app.include_router(router=ir_router, prefix=url_with_prefix(), tags=['Внесение-Изъятие налички'])
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Cashbox",
#         description="Кассовый модуль. Работает c mongoDB, fastAPI",
#         version="1.0",
#         routes=app.routes,
#     )
#     _schema = CashboxExceptionSchema.schema()
#     _schemas = openapi_schema.setdefault('components', {}).setdefault('schemas', {})
#     _schemas.setdefault(_schema['title'], _schema)
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
#
#
# app.openapi = custom_openapi
