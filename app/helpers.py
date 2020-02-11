import json
import math
from uuid import uuid4
from datetime import timezone
from os import popen
from typing import Dict

from pydantic import BaseModel, Field
from aiohttp import ClientError, ClientSession
from app.exceptions import CashboxException


def round_half_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n*multiplier - 0.5) / multiplier


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def utc_to_local(utc_datetime):
    return utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)


def config_from_json_file(json_filename):

    _temp = {}
    with open(json_filename, 'r') as _file:
        _temp = json.load(_file)

    class JsonConfig(BaseModel):
        shopNumber: int = Field(..., title='Номер магазина', ge=0)
        department: int = Field(..., title='Номер дапартамента', ge=0)
        # timezone: str = Field(..., title='Часовой пояс')
        cashName: str = Field(..., title='Название кассы', min_length=3)
        comport: str = Field(..., title='Номер COM порта (COM9 для примера)', min_length=4)
        comportSpeed: int = Field(..., title='Скорость COM порта', gt=0)

    _config = JsonConfig(**_temp).dict()
    # print('config ', _config)
    return _config


async def make_request(url: str, method: str, data) -> Dict:
    try:
        async with ClientSession() as session:
            async with session.request(method, url, json=data) as result:
                if result.status >= 400:
                    err = await result.text()
                    raise CashboxException(data=err)
                return await result.json()
        # result = await app.aiohttp_requests.request(method, url, json=data)
    except ClientError as exc:
        raise CashboxException(data=str(exc))


async def request_to_paygate(url: str, method: str, data: Dict) -> Dict:
    content = await make_request(url, method, data)
    if content['statusCode'] != 200:
        msg = f'Paygate вернул код ответа 500. Сообщение: {content["errorMessage"]}'
        raise CashboxException(data=msg)
    return content


def get_WIN_UUID():
    return str(popen('wmic diskdrive get serialNumber').read())\
        .strip('SerialNumber')\
        .strip('\a')\
        .strip('\t')\
        .strip()


def get_cheque_number(string):
    return int(str(string).rsplit('.', maxsplit=1)[-1])


def generate_internal_order_id():
    return str(uuid4())
