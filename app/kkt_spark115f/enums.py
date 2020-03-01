from enum import IntEnum

"""
    Некоторые значения вызова функций

    obj.GetTextDeviceInfo(4) - дата и время вида '29-02-20 16:45:45'
    obj.GetTextDeviceInfo(6) - РН ККТ (регистрационный номер?)
    obj.GetTextDeviceInfo(5) - № фискалька (заводской номер?)
    obj.GetTextDeviceInfo(7) - ИНН
    obj.GetTextDeviceInfo(8) - Номер смены
    obj.GetTextDeviceInfo(12) - Номер последнего документа
    obj.GetTextDeviceInfo(14) - Номер ФН
    obj.GetTextDeviceInfo(17) - Время открытия смены
    obj.GetTextDeviceInfo(28) - Похоже на количество денег в ящике
"""


class KKTInfoEnum(IntEnum):
    current_time_and_date = 4
    factory_number = 5
    reg_number = 6
    inn = 7
    shift_number = 8
    last_doc_number = 12
    fiscal_memory_device_number = 14
    shift_open_close_time = 11
    current_cash_balance = 28

    def __get__(self, instance, owner):
        return self.value

