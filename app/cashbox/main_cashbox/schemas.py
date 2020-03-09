from pydantic import Field, BaseModel
from app.schemas import DefaultSuccessResponse, CashierData


class RequestRegisterCashboxCharacter(BaseModel):
    character: str = Field(..., title='Символ кассы. Необходим для совершения заказа', min_length=1)


class ResponseRegisterCashboxCharacter(DefaultSuccessResponse, RequestRegisterCashboxCharacter):
    msg: str = Field('Символ кассы сохранен', title='Сообщение об успешном сохранении символа кассы')


class ResponseGetSystemID(DefaultSuccessResponse):
    device_id: str = Field(..., title='Идентификатор устройства')


class RequestRegisterFiscalCashier(CashierData):
    fiscal_cashier_fio: str = Field(..., title='ФИО кассира для регистрации в фискальнике',
                                    min_length=3, max_length=34)
    fiscal_cashier_password: str = Field(..., title='Пароль кассира в фискальнике (только цифры)',
                                         min_length=5, max_length=5)


class ResponseRegisterFiscalCashier(DefaultSuccessResponse):
    msg: str = Field('Зарегистрирован успешно', title='Сообщение об успешном регистрировании кассира '
                                                      'в фискальном регистраторе')
