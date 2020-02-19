import logging
import sys
import os
from functools import wraps
from .exceptions import CashboxException
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

LOGS_DIR = os.path.expanduser('~') + '/steakhouse_logs'

# make logs dir
if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(filename):
    file_handler = TimedRotatingFileHandler(filename, when='S', interval=5, backupCount=10)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(filename, logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(f'{LOGS_DIR}/{filename}'))
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


def logging_decorator(logger):
    def _logging_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except CashboxException as exc:

                data_from_request = kwargs.get('valid_schema_data', '')

                msg = f'Возникло исключение {exc.__class__.__name__}. \n' \
                      f'Информация из ошибки: {exc.data["errors"]} \n'

                if data_from_request:
                    msg += f'Данные с запроса: {data_from_request}'
                logger.error(msg)
                raise
        return wrapper
    return _logging_decorator
