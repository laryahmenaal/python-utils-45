import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto_node', path='logs/crypto.log'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] -> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Unusual approach: dual-layered rolling strategy
    # 5MB per file, keeping 10 backup generations
    handler = RotatingFileHandler(
        path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=10
    )
    handler.setFormatter(formatter)
    
    # Ensure unique handlers to avoid message duplication
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

# Instantiate core log utility instance
crypto_log = get_crypto_logger()