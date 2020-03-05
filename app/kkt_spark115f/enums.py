from enum import IntEnum


class KKTInfoEnum(IntEnum):
    current_time_and_date = 4
    factory_number = 5
    reg_number = 6
    inn = 7
    shift_number = 8
    shift_open_close_time = 11
    last_doc_number = 12
    fiscal_memory_device_number = 14
    last_fiscal_doc_number = 19
    current_cash_balance = 28
    transaction_sum = 34

    def __get__(self, instance, owner):
        return self.value
