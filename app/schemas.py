from typing import List

from pydantic import BaseModel, Field


class CashboxExceptionSchema(BaseModel):
    error: bool = Field(True, title='Что-то пошло не так. Например, не найден ID сущности в базе')
    errors: List[str] = Field(..., title='Описание ошибок')
