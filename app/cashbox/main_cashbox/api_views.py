from fastapi import APIRouter
from .schemas import RequestRegisterCashboxCharacter, ResponseRegisterCashboxCharacter
from .doc_kwargs import doc_register_character
from .functions import register_cashbox_character


router = APIRouter()


@router.post('/register_character', **doc_register_character)
async def register_character(character: RequestRegisterCashboxCharacter):
    kwargs = {'valid_schema_data': character.dict()}
    data = await register_cashbox_character(**kwargs)
    return ResponseRegisterCashboxCharacter(**data)
