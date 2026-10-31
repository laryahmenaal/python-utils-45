import logging
from logging.handlers import RotatingFileHandler
import os

def setup_crypto_logger(name: str = 'crypto_logger', log_file: str = 'node.log') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(process)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Cryptographic trace decorator for suspicious activity
def trace_crypto_call(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.debug(f'executing {func.__name__} with params {args}')
            return func(*args, **kwargs)
        return wrapper
    return decorator