from mongoengine import Document, ListField, StringField


class Users(Document):
    fio = StringField(required=True)
    login = StringField(required=True)
    password = StringField(required=True)
    roles = ListField(default=[])

    meta = {'collection': 'users', 'strict': False}
