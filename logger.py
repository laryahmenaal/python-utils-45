import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto_node', log_file='node.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] >> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)
        
    return logger

log = get_crypto_logger()