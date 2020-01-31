

# ERROR MESSAGES

# if connected fiscal id not match actual fiscal id in db
ERR_IF_FISCAL_ID_NOT_SYNCED = """
Номер подключенного фискального регистратора 
и последнего использованного не совпадают!
Перезапустите приложение и 
попытайтесь закрыть смену и откройте снова
"""

# if shift number doesn't match fiscal shift number
ERR_SHIFT_NUMBER_NOT_SYNCED = """
Номер текущей смены на фискальном регистраторе и номер
текущей смены в базе данных не совпадает. 
Закройте смену и откройте снова """

# if shift fiscal shift is opened, but not opened in db
ERR_FISCAL_SHIFT_OPENED_BUT_NOT_IN_DB = """
Смена на фискальном регистраторе открыта, 
но не открыта в базе данных
"""

# if shift in db is opened but not in fiscal
ERR_DB_SHIFT_OPENED_BUT_NOT_IN_FISCAL = """
Смена открыта в базе данных, но не 
в фискальном регистраторе. Откройте смену
"""


ERR_MSG_IF_FISCAL_ERR_MSG_IS_BLANK = """
Текст ошибки отсутствует
"""