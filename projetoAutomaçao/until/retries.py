# utils/retries.py
import time
from functools import wraps

def retry(max_tentativas=3, delay=2, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for tentativa in range(1, max_tentativas + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Tentativa {tentativa} falhou: {e}")
                    if tentativa == max_tentativas:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
