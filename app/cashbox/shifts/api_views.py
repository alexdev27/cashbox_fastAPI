from fastapi import APIRouter
from .doc_kwargs import doc_open_shift, doc_close_shift, doc_current_shift_info
from .schemas import RequestOpenShift, RequestCloseShift

router = APIRouter()


@router.post('/open_shift', **doc_open_shift)
async def open_shift(data: RequestOpenShift):
    pass


@router.post('/close_shift', **doc_close_shift)
async def close_shift(data: RequestCloseShift):
    pass


@router.get('/shift_info', **doc_current_shift_info)
async def current_shift_info():
    pass

