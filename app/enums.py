from enum import IntEnum, Enum
from collections import namedtuple


_ = namedtuple('tax', ['fiscal_key', 'cashbox_key'])


class FiscalTaxesNumbers(IntEnum):
    tax_10_percent = 1
    tax_20_percent = 0


class CashboxTaxesNumbers(IntEnum):
    tax_10_percent = 10
    tax_20_percent = 20


# class Taxes(Enum):
#     tax_10 = _('1', 10)
#     tax_20 = _('0', 20)
#
#     @staticmethod
#     def get_fiscal_keys():
#         return [
#             int(Taxes.tax_10.value.fiscal_key),
#             int(Taxes.tax_20.value.fiscal_key)
#         ]


class CashPayment(IntEnum):
    """ Тип оплаты: Наличный расчет """
    CASH = 0


class NonCashPayment(IntEnum):
    """ Тип оплаты: Безналичный расчет """
    NON_CASH = 1


class PaymentChoices(IntEnum):
    CASH = CashPayment.CASH
    NON_CASH = NonCashPayment.NON_CASH


class PaymentDocumentType(IntEnum):
    """ Тип документа: Оплата """
    PAYMENT = 2


class ReturnDocumentType(IntEnum):
    """ Тип документа: Возврат """
    RETURN = 3


class InsertDocumentType(IntEnum):
    """ Тип документа: Внесение """
    INSERT = 4


class RemoveDocumentType(IntEnum):
    """ Тип документа: Изъятие """
    REMOVE = 5


class DocumentTypes(IntEnum):
    PAYMENT = PaymentDocumentType.PAYMENT
    RETURN = ReturnDocumentType.RETURN
    INSERT = InsertDocumentType.INSERT
    REMOVE = RemoveDocumentType.REMOVE




