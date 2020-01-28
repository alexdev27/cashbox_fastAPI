from fastapi import APIRouter
from .doc_kwargs import doc_open_shift
from .schemas import RequestOpenShift

router = APIRouter()


@router.post('/open_shift', **doc_open_shift)
def close_current_shift(data: RequestOpenShift):
    pass
