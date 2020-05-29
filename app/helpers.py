import json
import math
from enum import Enum
from uuid import uuid4
from datetime import timezone
from os import popen
from typing import Dict
from aiohttp import ClientError, ClientSession
from app.exceptions import CashboxException
from app.schemas import JsonConfig


def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper


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

    _config = JsonConfig(**_temp).dict()

    # quick hack. include other fields to result, if there is any
    for key in _temp.keys():
        if key not in _config.keys():
            _config[key] = _temp[key]
    return _config


async def make_request(url: str, method: str, data, do_raise=True) -> Dict:
    try:
        async with ClientSession() as session:
            async with session.request(method, url, json=data) as result:
                if result.status >= 400:
                    err = await result.text()
                    raise CashboxException(data=err)
                return await result.json()
        # result = await app.aiohttp_requests.request(method, url, json=data)
    except ClientError as exc:
        if do_raise:
            msg = f'Класс ошибки: {exc.__class__}; Детали ошибки: {str(exc)}'
            raise CashboxException(data=msg)
        else:
            return


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
