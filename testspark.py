from pprint import pprint as pp
from comtypes.client import CreateObject
from comtypes.gen._445B09C3_EF00_47B4_9DB0_68DDD7AA9FF1_0_1_0 import FPSpark, IFPSpark

obj = CreateObject(FPSpark, None, None, IFPSpark)


try:
    ""
    obj.DeinitDevice()

    pp(obj.InitDevice())

    # for i in range(1, 41):
    #     print(f'{i} -> result {obj.GetTextDeviceInfo(i)}')

    # pp(obj.SetCashier('1', '11115', 'Golushko.'))
    pp(obj.RegCashier('11115'))
    # pp(obj.ChkShift())
    # pp(obj.ChkCDrw())
    # pp(obj.OpenShift(12, "11112"))
    #
    pp(obj.CashIn(8, "1235"))


    pp(obj.GetTextDeviceInfo(0))
    # pp(obj.GetTextDeviceInfo(1))
    # pp(obj.GetTextDeviceInfo(2))
    # pp(obj.GetTextDeviceInfo(3))
    # pp(obj.GetTextDeviceInfo(4))
    # pp(obj.GetTextDeviceInfo(5))

    # pp(obj.OpenShift(12, "11111"))
    # pp(obj.CashIn(1, "1233"))
    # pp(obj.CloseShift())
    # pp(obj.CashIn(2, "1234"))
    # pp(obj.CashIn(8, "12355"))
    # pp(obj.ChkFS())
    # pp(obj.OpenCDrw())
    # pp(obj.GetExtendedErrorComment(-3))
    # pp(obj.GetExtendedErrorComment(10))
    # pp(obj.GetExtendedErrorComment(21))
    obj.DeinitDevice()


except Exception as e:
    print('+++++++++++++')
    print(e)

# PumpEvents(300)
"""
    Некоторые значения вызова функций
    
    obj.GetTextDeviceInfo(4) - дата и время вида '29-02-20 16:45:45'
    obj.GetTextDeviceInfo(6) - РН ККТ (регистрационный номер?)
    obj.GetTextDeviceInfo(5) - № фискалька (заводской номер?)
    obj.GetTextDeviceInfo(7) - ИНН
    obj.GetTextDeviceInfo(8) - Похоже не номер смены
    obj.GetTextDeviceInfo(14) - ФН
    obj.GetTextDeviceInfo(28) - Похоже на счетчик внесения
"""
