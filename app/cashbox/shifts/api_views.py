from fastapi import APIRouter
from .doc_kwargs import doc_open_shift, doc_close_shift, doc_current_shift_info
from .schemas import RequestOpenShift, RequestCloseShift, \
    ResponseCloseShift, ResponseOpenShift, ResponseCurrentShiftInfo
from .functions import close_current_shift, open_new_shift, get_shift_info

router = APIRouter()


@router.post('/open_shift', **doc_open_shift)
async def open_shift(data: RequestOpenShift):
    kwargs = {'valid_schema_data': data.dict()}
    resp_data = await open_new_shift(**kwargs)
    resp_data = {'lol': 'kek'}
    # return ResponseOpenShift(**resp_data)
    return ResponseOpenShift(**resp_data)


@router.post('/close_shift', **doc_close_shift)
async def close_shift(data: RequestCloseShift):
    kwargs = {'valid_schema_data': data.dict()}
    resp_data = close_current_shift(**kwargs)
    return ResponseCloseShift(**resp_data)


@router.get('/shift_info', **doc_current_shift_info)
async def current_shift_info():
    resp_data = get_shift_info()
    return ResponseCurrentShiftInfo(**resp_data)
