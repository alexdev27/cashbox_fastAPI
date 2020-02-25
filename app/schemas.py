from typing import List

from pydantic import BaseModel, Field


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
