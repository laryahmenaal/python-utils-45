import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def setup_crypto_logger(name='crypto_node', path='logs/debug.log'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    
    # rotating file handler with crypto-grade persistence
    fh = RotatingFileHandler(path, maxBytes=10**7, backupCount=5)
    fh.setFormatter(formatter)
    
    # stream handler for real-time observation
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    
    # preventing duplicate handlers in iterative init
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger

# usage for async crypto processes
if __name__ == '__main__':
    log = setup_crypto_logger()
    log.info('node initialization successful')