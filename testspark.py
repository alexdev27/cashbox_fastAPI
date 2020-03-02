from pprint import pprint as pp
from comtypes.client import CreateObject, GetModule
from comtypes.gen._445B09C3_EF00_47B4_9DB0_68DDD7AA9FF1_0_1_0 import FPSpark, IFPSpark
# from comtypes.gen._CF921C08_02B9_415D_84C9_BA2ACE7C20AF_0_1_0 import \
#     SAPacketObj, ISAPacketObj, PCPOSTConnectorObj, IPCPOSTConnectorObj

from ctypes import *


arcus = cdll.LoadLibrary(r"C:\Arcus2\DLL\arccom.dll")

obj = CreateObject(FPSpark, None, None, IFPSpark)


# def create_arcus():
#     return arcus.CreateITpos()
#
# def run_arcus():
#     pass
#
# def destroy_arcus():
#     return arcus.DeleteITPos()



# pp(arcus.CreateITPos)
# sap = CreateObject(SAPacketObj, None, None, ISAPacketObj)
# pos = CreateObject(PCPOSTConnectorObj)0


pos_obj = arcus.CreateITPos()
s = c_char_p(b'678')


arcus.ITPosSet(pos_obj, 'currency', byref(s), -1)
arcus.ITPosSet(pos_obj, 'amount', byref(s), -1)
#
a = arcus.ITPosRun(pos_obj, 1)

arcus.ITPosClear(pos_obj)
arcus.DeleteITPos(pos_obj)
#
# pp('run command')
# pp(a)











try:
    ""

    # obj.DeinitDevice()
    # pp(windll.kernel32)
    # pp(obj.InitDevice())
    # pp(obj.RegCashier('11115'))
    # pp(dir(arcus))
    # for i in range(1, 29):
    #     print(f'{i} -> result {obj.GetTextDeviceInfo(i)}')

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
    # pp(obj.CashIn(8, "12345"))


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
    # obj.DeinitDevice()


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
