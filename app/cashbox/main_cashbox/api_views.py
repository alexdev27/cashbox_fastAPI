from fastapi import APIRouter
from .schemas import RequestRegisterCashboxCharacter, ResponseRegisterCashboxCharacter
from .doc_kwargs import doc_register_character, doc_get_sys_id
from .functions import register_cashbox_character, get_sys_id


router = APIRouter()


@router.post('/register_character', **doc_register_character)
async def register_character(character: RequestRegisterCashboxCharacter):
    kwargs = {'valid_schema_data': character.dict()}
    data = await register_cashbox_character(**kwargs)
    return ResponseRegisterCashboxCharacter(**data)


# @router.post('/register_fiscal_cashier', **doc_register_fiscal_cashier)
# async def register_cashier(cashier_data: RequestRegisterFiscalCashier):
#     kwargs = {'valid_schema_data': cashier_data.dict()}
#     data = await register_fiscal_cashier(**kwargs)
#     return ResponseRegisterFiscalCashier(**data)
#

@router.get('/get_system_id', **doc_get_sys_id)
def get_system_id():
    return get_sys_id()
