from fastapi import APIRouter
from .schemas import RequestRegisterCashboxCharacter
from .doc_kwargs import doc_register_character
# from .functions import


router = APIRouter()


@router.post('register_character', **doc_register_character)
def register_character(character: RequestRegisterCashboxCharacter):
    pass