from typing import List

from pydantic import Field, BaseModel
from app.enums import UserRoles


class BaseFields:
    fio: str = Field(default='', title='ФИО пользователя')
    fio_required: str = Field(..., title='ФИО пользователя', min_length=3)
    login: str = Field(default='', title='Идентификатор пользователя')
    login_required: str = Field(..., title='Идентификатор пользователя', min_length=3)
    password: str = Field(default='', title='Пароль пользователя (будет зашифрован)')
    password_required: str = Field(..., title='Пароль пользователя (будет зашифрован)', min_length=4)
    roles: List[UserRoles] = Field(default=[], title='Роли пользователя')
    roles_required: List[UserRoles] = Field(..., title='Роли пользователя')


class AllRequired(BaseModel):
    fio: str = BaseFields.fio_required
    login: str = BaseFields.login_required
    roles: List[UserRoles] = BaseFields.roles_required


class EngineerUserRequired(BaseModel):
    engineer_login: str = Field(..., title='Логин инженера')
    engineer_password: str = Field(..., title='Пароль инженера')


class RequestCreateUser(EngineerUserRequired, AllRequired):
    password: str = BaseFields.password_required


class RequestGetUser(EngineerUserRequired):
    id: str


class RequestGetUsers(EngineerUserRequired):
    pass


# class

