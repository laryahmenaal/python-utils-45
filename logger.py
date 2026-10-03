import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str = 'crypto_core', log_file: str = 'crypto.log'):
    """ Initialize rotating logger with a creative format """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Ensuring standard log directory exists
    os.makedirs('logs', exist_ok=True)
    path = os.path.join('logs', log_file)
    
    # Handler with 1MB rotation and 3 backup files
    handler = RotatingFileHandler(path, maxBytes=1024*1024, backupCount=3)
    formatter = logging.Formatter(
        '[%(asctime)s][%(levelname)s] << %(name)s >> :: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Prevent duplicate handlers if re-initialized
    if not logger.handlers:
        logger.addHandler(handler)
        
    # Console echo for visible crypto flow
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Instantiate for quick access
log = get_crypto_logger()