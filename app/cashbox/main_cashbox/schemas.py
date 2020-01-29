from pydantic import Field
from app.schemas import DefaultSuccessResponse


class RequestRegisterCashboxCharacter(DefaultSuccessResponse):
    character: str = Field(..., title='Символ кассы. Необходим для совершения заказа', min_length=1)


class ResponseRegisterCashboxCharacter(RequestRegisterCashboxCharacter):
    msg: str = Field('Символ кассы сохранен', title='Сообщение об успешном сохранении символа кассы')


class ResponseGetSystemID(DefaultSuccessResponse):
    device_id: str = Field(..., title='Идентификатор устройства')
