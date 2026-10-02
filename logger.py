import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str, log_file: str = 'crypto_node.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

class SecureLoggerWrapper:
    def __init__(self, name):
        self._log = get_crypto_logger(name)

    def trace(self, msg: str):
        self._log.debug(f'TRACE: {msg}')

    def alert(self, msg: str):
        self._log.critical(f'ALERT: {msg}')