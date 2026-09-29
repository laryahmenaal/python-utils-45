import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str = 'crypto_bot', log_file: str = 'audit.log') -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # Rotation logic for high-frequency transaction logs
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=10 * 1024 * 1024, 
        backupCount=5
    )
    
    # Custom level-based filtering for sensitive crypto operations
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    # Console output for active monitoring
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)
    
    return logger

# Instantiate for quick access
logger = get_crypto_logger()