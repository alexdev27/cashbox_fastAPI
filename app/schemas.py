from typing import List, Dict, Union

from pydantic import BaseModel, Field


class CashboxExceptionSchema(BaseModel):
    error: bool = Field(True, title='Что-то пошло не так. Например, не найден ID сущности в базе')
    errors: List[str] = Field(..., title='Описание ошибок')


class CashierData(BaseModel):
    cashier_name: str = Field(..., title='ФИО даныые кассира', min_length=3)
    cashier_id: str = Field(..., title='Идентификатор кассира', min_length=3)


class DefaultSuccessResponse(BaseModel):
    error: bool = False
    # data: Union[Dict, List, str]