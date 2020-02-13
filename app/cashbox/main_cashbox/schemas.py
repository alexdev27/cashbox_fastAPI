from pydantic import Field, BaseModel
from app.schemas import DefaultSuccessResponse


class RequestRegisterCashboxCharacter(BaseModel):
    character: str = Field(..., title='Символ кассы. Необходим для совершения заказа', min_length=1)


class ResponseRegisterCashboxCharacter(DefaultSuccessResponse, RequestRegisterCashboxCharacter):
    msg: str = Field('Символ кассы сохранен', title='Сообщение об успешном сохранении символа кассы')


class ResponseGetSystemID(DefaultSuccessResponse):
    device_id: str = Field(..., title='Идентификатор устройства')
