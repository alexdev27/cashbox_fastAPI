from pprint import pprint as pp
from comtypes.client import CreateObject
from comtypes.gen._445B09C3_EF00_47B4_9DB0_68DDD7AA9FF1_0_1_0 import FPSpark, IFPSpark
obj = CreateObject(FPSpark, None, None, IFPSpark)


try:
    ""
    # obj.DeinitDevice()

    pp(obj.InitDevice())
    pp(obj.RegCashier('11115'))

    for i in range(-800, -100):
        print(f'{i} -> result {obj.GetTextDeviceInfo(i)}')

    # pp(obj.SetCashier('1', '11115', 'Golushko.'))
    # pp(obj.SetCashier('1', '11115', 'Чебуречкин А. П.'))
    # pp(obj.RegCashier('11115'))
    # pp(obj.ChkShift())
    # pp(obj.ChkCDrw())
    # pp(obj.GetExtendedErrorCode())
    # exit()
    # pp('++++++++++++++++++++++')
    # pp(obj.GetTextDeviceInfo(0))
    # pp(obj.CashIn(8, "12345"))
    # pp(obj.CashOut(8, "147"))

    # pp(obj.CloseShift())
    #
    # pp(obj.OpenShift(1231, "11115"))


    # pp('++++++++++++++++++++++')
    # pp(obj.GetTextDeviceInfo(0))
    # for i in range(1, 29):
    #
    #     print(i, str(obj.GetTextDeviceInfo(i)).strip())
    # pp('-----------------------')
    # pp(obj.GetTextDeviceInfo(0))
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
    obj.GetTextDeviceInfo(8) - Номер смены
    obj.GetTextDeviceInfo(11) - Время открытия смены
    obj.GetTextDeviceInfo(12) - Номер последнего документа
    obj.GetTextDeviceInfo(14) - Номер ФН
    obj.GetTextDeviceInfo(28) - Похоже на количество денег в ящике
"""
