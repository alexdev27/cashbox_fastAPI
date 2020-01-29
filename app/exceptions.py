from typing import Dict, List, Union
from .schemas import CashboxExceptionSchema
from app import app
from starlette.requests import Request
from starlette.responses import JSONResponse


class CashboxException(Exception):
    def __init__(self, *, data: Union[str, List[str]], status_code: int = 400):
        errs = []
        if isinstance(data, (list,)):
            errs.extend(data)
        elif isinstance(data, (str,)):
            errs.append(data)

        self.data: Dict = CashboxExceptionSchema(errors=errs).dict()
        self.status_code = status_code


@app.exception_handler(CashboxException)
async def handle_cashbox_exception(req: Request, exc: CashboxException):
    return JSONResponse(content=exc.data, status_code=exc.status_code)
