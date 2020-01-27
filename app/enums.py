from enum import IntEnum, Enum
from collections import namedtuple


_ = namedtuple('tax', ['fiscal_key', 'cashbox_key'])


class Taxes(Enum):
    tax_10 = _('1', 10)
    tax_20 = _('0', 20)

    @staticmethod
    def get_fiscal_keys():
        return [
            int(Taxes.tax_10.value.fiscal_key),
            int(Taxes.tax_20.value.fiscal_key)
        ]


class PaymentTypes(IntEnum):
    _cash = 0
    _non_cash = 1


class DocumentTypes(IntEnum):
    _payment = 2
    _return = 3
    _insert = 4
    _remove = 5

