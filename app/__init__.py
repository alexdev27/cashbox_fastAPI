from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from aiohttp import ClientSession
from .schemas import CashboxExceptionSchema
from .cashbox.insert_remove.api_views import router as insert_remove_router
from .cashbox.shifts.api_views import router as shifts_router
from .cashbox.orders.api_views import router as orders_router
from .cashbox.main_cashbox.functions import init_cashbox
from .custom_responses import response_400
from .exceptions import CashboxException
from mongoengine import connect, disconnect
import config

# mongo connection
connect(
    db=config.MONGODB_SETTINGS['DB'],
    host='localhost',
    port=27017
)

app = FastAPI()

aiohttp_requests = ClientSession()

default_prefix = '/api'


def url_with_prefix(url: str = '') -> str:
    return f'{default_prefix}{url}'


app.include_router(
    router=insert_remove_router,
    prefix=url_with_prefix(),
    responses=response_400,
    tags=['Операции внесения-изъятия налички'])

app.include_router(
    router=shifts_router,
    prefix=url_with_prefix(),
    responses=response_400,
    tags=['Операции со сменой'])

app.include_router(
    router=orders_router,
    prefix=url_with_prefix(),
    responses=response_400,
    tags=['Заказы (совершение оплаты/отмены)'])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Cashbox",
        description="Кассовый модуль. Работает c mongoDB, fastAPI",
        version="1.0",
        routes=app.routes,
    )
    _schema = CashboxExceptionSchema.schema()
    _schemas = openapi_schema.setdefault('components', {}).setdefault('schemas', {})
    _schemas.setdefault(_schema['title'], _schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(CashboxException)
async def handle_cashbox_exception(req: Request, exc: CashboxException):
    return JSONResponse(content=exc.data, status_code=exc.status_code)


@app.on_event('startup')
async def async_startup():
    await init_cashbox()


@app.on_event('shutdown')
async def async_shutdown():
    await aiohttp_requests.close()


@app.on_event('shutdown')
def sync_shutdown():
    disconnect()

