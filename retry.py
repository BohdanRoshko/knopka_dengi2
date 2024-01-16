from loguru import logger
from sys import stderr
from time import sleep

# from urllib3.exceptions import MaxRetryError
from requests.exceptions import ProxyError

from settings import MAX_RETRIES

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{message}</level>")


def retry(times=MAX_RETRIES, exceptions=(ProxyError)):
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    logger.error(f'ERROR {func.__name__}: {err} [{attempt+1}/{times}]')
                    attempt += 1
                    sleep(5)
            return func(*args, **kwargs)
        return newfn
    return decorator
