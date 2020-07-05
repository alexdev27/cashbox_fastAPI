from typing import List, Optional

from pydantic import Field, BaseModel
from app.enums import UserRoles
from app.custom_types import ObjectIdStr


class BaseFields:
    id: ObjectIdStr = Field(default='', title='ID пользователя в базе')
    id_required: ObjectIdStr = Field(..., title='ID пользователя в базе')
    fio: str = Field(default='', title='ФИО пользователя', min_length=3)
    fio_required: str = Field(..., title='ФИО пользователя', min_length=3)
    login: str = Field(default='', title='Идентификатор пользователя', min_length=3)
    login_required: str = Field(..., title='Идентификатор пользователя', min_length=3)
    password: str = Field(default='', title='Пароль пользователя', min_length=4)
    password_required: str = Field(..., title='Пароль пользователя', min_length=4)
    roles: List[UserRoles] = Field(default=[], title='Роли пользователя', min_items=1)
    roles_required: List[UserRoles] = Field(..., title='Роли пользователя', min_items=1)


class AllRequired(BaseModel):
    fio: str = BaseFields.fio_required
    login: str = BaseFields.login_required
    roles: List[UserRoles] = BaseFields.roles_required


class AllOptional(BaseModel):
    fio: Optional[str] = BaseFields.fio
    login: Optional[str] = BaseFields.login
    roles: Optional[List[UserRoles]] = BaseFields.roles


class EngineerUserCredentials(BaseModel):
    engineer_login: str = Field(..., title='Логин инженера')
    engineer_password: str = Field(..., title='Пароль инженера')


class RequestCreateUser(AllRequired):
    password: str = BaseFields.password_required


class ResponseCreateUser(AllRequired):
    class Config:
        orm_mode = True


class ResponseGetUser(AllRequired):
    id: ObjectIdStr = BaseFields.id

    class Config:
        orm_mode = True


class ResponseGetUsers(BaseModel):
    result: List[ResponseGetUser] = Field(..., title='Пользователи')


# class UserForView(BaseModel):
#     id: ObjectIdStr = BaseFields.id_required
#     fio: str
#     roles: List[UserRoles]
#     login: str


# class RequestGetUsers(BaseModel):
#     users: List[]


class RequestModifyUser(AllOptional):
    password: Optional[str] = BaseFields.password




