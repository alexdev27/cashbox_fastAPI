from os import popen
from typing import Dict, List

import app
from pydantic import BaseModel, Field, HttpUrl
import json
from aiohttp import ClientError
from app.exceptions import CashboxException


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
        result = await app.aiohttp_requests.request(method, url, json=data)
    except ClientError as exc:
        raise CashboxException(data=str(exc))

    if result.status >= 400:
        err = await result.text()
        raise CashboxException(data=err)
    return await result.json()


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
