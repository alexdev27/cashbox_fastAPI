from enum import IntEnum, Enum


class AllowedDevices(str, Enum):
    pirit2f = 'pirit2f'
    spark115f = 'spark115f'

    def __get__(self, instance, owner):
        return self.value


class PaygateURLs(Enum):
    new_order = '/createorder'
    cancel_order = '/cancelpay'
    open_shift = '/openshift'
    close_shift = '/closeshift'
    insert_cash = '/cashin'
    remove_cash = '/cashout'
    register_cash = '/regcash'
    refund_part = '/refundpay'
    check_order_status = '/checkstatus'

    def __get__(self, instance, owner):
        return self.value


class FiscalTaxesNumbers(IntEnum):
    tax_10_percent = 1
    tax_20_percent = 0


class CashboxTaxesNumbers(IntEnum):
    tax_10_percent = 10
    tax_20_percent = 20


# def get_cashbox_tax_from_fiscal_tax(num: int):
#     if FiscalTaxesNumbers.tax_10_percent == num:
#         return CashboxTaxesNumbers.tax_10_percent.value
#     elif FiscalTaxesNumbers.tax_20_percent == num:
#         return CashboxTaxesNumbers.tax_20_percent.value
#     else:
#         return CashboxTaxesNumbers.tax_20_percent.value


def get_fiscal_tax_from_cashbox_tax(num: int):
    if CashboxTaxesNumbers.tax_10_percent == num:
        return FiscalTaxesNumbers.tax_10_percent.value
    elif CashboxTaxesNumbers.tax_20_percent == num:
        return FiscalTaxesNumbers.tax_20_percent.value
    else:
        return FiscalTaxesNumbers.tax_20_percent.value


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
