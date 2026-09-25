import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str = 'crypto_node', path: str = 'logs/node.log') -> logging.Logger:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Unusual approach: format using custom cryptographic-style prefixing
    formatter = logging.Formatter('[%(asctime)s][HEX-0x%(process)X][%(levelname)s] %(message)s')
    
    # Rotation at 5MB, keep 3 backup files
    handler = RotatingFileHandler(
        path, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        # Add console output for local development visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

# Instantiate for crypto module usage
logger = get_crypto_logger()