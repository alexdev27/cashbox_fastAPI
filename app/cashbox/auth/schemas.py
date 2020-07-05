from app.schemas import DefaultSuccessResponse


class Token(DefaultSuccessResponse):
    access_token: str
    token_type: str = 'Bearer'
