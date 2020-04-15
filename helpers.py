from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)

def with_logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'started {func.__name__}')
        f = func(*args, **kwargs)
        logging.info(f'ended {func.__name__} successfully!')
        return f
    return wrapper