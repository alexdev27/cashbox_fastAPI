from typing import Dict, List, Union
from .schemas import CashboxExceptionSchema


class CashboxException(Exception):
    def __init__(self, *, data: Union[str, List[str]], status_code: int = 400, to_logging=None):

        errs = []
        if isinstance(data, (list,)):
            errs.extend(data)
        elif isinstance(data, (str,)):
            errs.append(data)

        self.data: Dict = CashboxExceptionSchema(errors=errs).dict()
        self.status_code = status_code
        self.to_logging = to_logging

    def __str__(self):
        return self.data['errors'][0]
