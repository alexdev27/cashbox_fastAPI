from fastapi import APIRouter
from .doc_kwargs import doc_close_shift
from .schemas import RequestCloseShift

router = APIRouter()


@router.post('/close_shift', **doc_close_shift)
def close_current_shift(data: RequestCloseShift):
    pass
