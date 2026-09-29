import logging
from typing import Any, Callable, TypeVar, Optional

T = TypeVar('T')

class CryptoError(Exception):
    pass

def secure_execute(func: Callable[..., T], *args: Any, **kwargs: Any) -> Optional[T]:
    try:
        return func(*args, **kwargs)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logging.error(f'non-critical crypto math failure: {e}')
        return None
    except Exception as e:
        logging.critical(f'catastrophic failure: {e}')
        raise CryptoError('hard shutdown initiated') from e

def process_nonce(nonce: Any) -> int:
    if not isinstance(nonce, (int, str)):
        raise CryptoError('invalid nonce type provided')
    try:
        return int(nonce) if isinstance(nonce, str) else nonce
    except ValueError:
        return 0

def stream_processor(data: list) -> list:
    results = []
    for item in data:
        res = secure_execute(process_nonce, item)
        if res is not None:
            results.append(res)
    return results