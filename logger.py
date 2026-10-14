import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name='crypto_node', log_file='node.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # ensure log directory existence
    os.makedirs('logs', exist_ok=True)
    log_path = os.path.join('logs', log_file)
    
    # rotate at 5MB, keep 5 backups
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5*1024*1024, 
        backupCount=5
    )
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [nonce:%(process)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        # extra console bridge for dev ops visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger