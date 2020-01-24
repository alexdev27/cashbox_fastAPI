from typing import Dict, List, Union

from .schemas import CashboxExceptionSchema


class CashboxException(Exception):
    def __init__(self, *, data: Union[str, List[str]], status_code: int = 400):
        errs = []
        if isinstance(data, (list,)):
            errs.extend(data)
        elif isinstance(data, (str,)):
            errs.append(data)

        self.data: Dict = CashboxExceptionSchema(errors=errs).dict()
        self.status_code = status_code
