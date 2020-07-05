import sys
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)


from config import CASH_SETTINGS
from .enums import AllowedDevices

if CASH_SETTINGS['deviceName'] == AllowedDevices.pirit2f:
    from app.kkt_device.models import Pirit2f
    KKTDevice = Pirit2f
elif CASH_SETTINGS['deviceName'] == AllowedDevices.spark115f:
    from app.kkt_spark115f.models import Spark115f
    KKTDevice = Spark115f
else:
    exit(f"Неизвестное имя устройства {CASH_SETTINGS['deviceName']}")

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from celery import Celery
from redis import Redis
from .schemas import CashboxExceptionSchema
from .cashbox.insert_remove.api_views import router as insert_remove_router
from .cashbox.shifts.api_views import router as shifts_router
from .cashbox.orders.api_views import router as orders_router
from .cashbox.main_cashbox.api_views import router as cashbox_router
from .cashbox.users.api_views import users_router
from .cashbox.auth.api_views import auth_router
from .cashbox.main_cashbox.functions import init_cashbox
from .custom_responses import response_400
from .exceptions import CashboxException
from mongoengine import connect, disconnect
import config
from .logging import get_logger


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# mongo connection
connect(
    db=config.MONGODB_SETTINGS['DB'],
    host='localhost',
    port=27017
)

celery = Celery('CeleryApp', broker=config.CELERY_BROKER_URL,
                backend=config.CELERY_RESULT_BACKEND)
redis = Redis(host=config.HOSTNAME)

redis.flushall()
app = FastAPI(title='Cashbox on steroids', docs_url=None, redoc_url=None)
app.mount('/static', StaticFiles(directory='app/static'), name='static')


default_prefix = '/api'


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


def url_with_prefix(url: str = '') -> str:
    return f'{default_prefix}{url}'


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#
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


app.include_router(
    router=users_router,
    prefix=url_with_prefix(),
    tags=['Операции с пользователями']
)

app.include_router(
    router=auth_router,
    prefix=url_with_prefix(),
    tags=['Авторизация']
)

app.include_router(
    router=cashbox_router,
    prefix=url_with_prefix(),
    tags=['Другие операции над кассой'])

# "hashed_password": "$2b$10$5AEINtothQlazoHtaYqjK.ztGYqsoDKhNNbGB1fyzFSoZXWpjOgP2",

# from typing import Optional
#
# from fastapi import Depends, FastAPI, HTTPException
# from starlette.status import HTTP_401_UNAUTHORIZED
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel
#
# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }
#
# app = FastAPI()
#
#
# def fake_hash_password(password: str):
#     return "fakehashed" + password
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
#
#
# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}
#
#
# @app.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


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
    startup_logger = get_logger('startup.log', 'startup_error_logger')
    try:
        await init_cashbox()
        KKTDevice.startup()
        #pass
    except CashboxException as c_exc:
        msg = f'{c_exc.__class__.__name__}: {c_exc.data["errors"]}'
        startup_logger.error(msg)
        sys.exit(msg)
    except Exception as exc:
        msg = str(exc)
        startup_logger.error(msg)
        sys.exit(msg)


@app.on_event('shutdown')
async def async_shutdown():
    pass


@app.on_event('shutdown')
def sync_shutdown():
    celery.control.purge()
    disconnect()

from .cashbox.main_cashbox.tasks import try_send_to_paygate
