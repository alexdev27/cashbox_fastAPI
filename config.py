

import sys
from os import environ as envs
from app.helpers import config_from_json_file
import json


SECRET_KEY = 'erg434gerg2425t23adrwerwffwer23qw42z'

MONGODB_SETTINGS = {
    'DB': 'temp_payment_data_2',
}

temp_payment_service_url = 'http://10.21.3.38:8100'

HOSTNAME = 'localhost'

REDIS_BACKEND = 'redis://{}:6379'.format(HOSTNAME)
CELERY_BROKER_URL = 'redis://{}:6379/1'.format(HOSTNAME)
CELERY_RESULT_BACKEND = 'redis://{}:6379/1'.format(HOSTNAME)
CELERY_IGNORE_RESULT = True
TIMEZONE = 'Asia/Vladivostok'

CASH_SETTINGS = {}
cash_settings_file = 'cash-conf.json'

DLL_PATH = envs.get('SPARK_DLL')

try:
    CASH_SETTINGS = config_from_json_file(cash_settings_file)
except FileNotFoundError as f_err:
    print(f'Файла {cash_settings_file} не существует. Создайте и заполните его')
    sys.exit()
except json.JSONDecodeError as j_err:
    print('Не правильный формат данных. Предоставьте валидный JSON')
    sys.exit()
except ValueError as v_err:
    print('Не удалось полностью прочитать конфиг. Ошибки:')
    print(v_err)
    sys.exit()
except Exception as err:
    print('Непредвиденное исключение: ')
    print(str(err))
    sys.exit()
