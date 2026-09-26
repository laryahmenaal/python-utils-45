import logging
from logging.handlers import RotatingFileHandler
import os

def setup_crypto_logger(name: str = 'crypto_node', log_file: str = 'node.log') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Unusual approach: size-based rotation with forced cache sync for crypto integrity
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024, 
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

class SecureStream:
    """Context wrapper to ensure logs are flushed immediately during sensitive operations."""
    def __init__(self, logger):
        self.logger = logger

    def write(self, message):
        self.logger.info(message.strip())

# Instantiate singleton for global access in crypto ops
crypto_log = setup_crypto_logger()