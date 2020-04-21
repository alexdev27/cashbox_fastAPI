from typing import List
from pytz import all_timezones
from ipaddress import IPv4Address, AddressValueError
from pydantic import BaseModel, Field, validator
from app.enums import AllowedDevices


class JsonConfig(BaseModel):
    shopNumber: int = Field(..., title='Номер магазина', ge=0)
    department: int = Field(..., title='Номер дапартамента', ge=0)
    paygateAddress: str = Field(..., title='IP сервера')
    timezone: str = Field(..., title='Часовой пояс')
    cashName: str = Field(..., title='Название кассы', min_length=3)
    deviceName: AllowedDevices = Field(..., title='Название устройства')

    @validator('timezone')
    def validate_timezone(cls, value):
        if value not in all_timezones:
            raise ValueError(f'\t-> Нет такого ({value}) часового пояса!')
        return value

    @validator('paygateAddress')
    def validate_paygate_address(cls, value):
        errstr = '-> Ошибка валидации paygateAddress: '
        if ':' not in value:
            raise ValueError(errstr + 'Отсутствует порт!')

        ip, port = str(value).rsplit(':', maxsplit=1)

        try:
            int(port)
        except ValueError as i_err:
            raise ValueError(errstr + f'Порт дожлжен быть числом! Получен {port}')

        # will fix later
        # try:
        #     IPv4Address(ip)
        # except AddressValueError as v_err:
        #     raise ValueError(errstr + f'Некоррестный формат IP адреса! Получен {ip}')

        return value


class CashboxExceptionSchema(BaseModel):
    from_cashbox: bool = Field(True, title='Флаг "это из кассы". Временный костыль')
    error: bool = Field(True, title='Что-то пошло не так. Например, не найден ID сущности в базе')
    errors: List[str] = Field(..., title='Описание ошибок')


class CashierData(BaseModel):
    cashier_name: str = Field(..., title='ФИО даныые кассира', min_length=2)
    cashier_id: str = Field(..., title='Идентификатор кассира', min_length=2)


class DefaultSuccessResponse(BaseModel):
    from_cashbox: bool = Field(True, title='Флаг "с кассы"')
    error: bool = Field(False, title='Флаг ошибки')
