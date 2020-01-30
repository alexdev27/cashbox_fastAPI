from enum import IntEnum, Enum


class PaygateURLs(Enum):
    new_order = '/createorder'
    cancel_order = '/cancelpay',
    open_shift = '/openshift',
    close_shift = '/closeshift',
    insert_cash = '/cashin',
    remove_cash = '/cashout'
    register_cash = '/regcash'


class FiscalTaxesNumbers(IntEnum):
    tax_10_percent = 1
    tax_20_percent = 0


class CashboxTaxesNumbers(IntEnum):
    tax_10_percent = 10
    tax_20_percent = 20


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
