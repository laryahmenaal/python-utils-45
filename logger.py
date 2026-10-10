import sys
import functools
import logging

class CryptoSafeLogger:
    def __init__(self, name='crypto-ops'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(handler)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                self.logger.error(f'Decryption mismatch in {func.__name__}: {e}')
                raise ConnectionAbortedError('Security constraint violated') from e
            except Exception as e:
                self.logger.critical(f'Catastrophic failure in {func.__name__}: {type(e).__name__}')
                return None
        return wrapper

    def audit(self, context: str, payload: bytes):
        if not isinstance(payload, bytes):
            self.logger.warning(f'Malformed audit signal: {context}')
            return False
        return True

crypto_logger = CryptoSafeLogger()