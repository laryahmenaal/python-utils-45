import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto_node'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # path normalization for platform agnostic crypto logging
    log_dir = os.path.join(os.path.expanduser('~'), '.crypto_utils')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f'{name}.log')

    # 5MB rotation policy with 3 historical backups
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )

    # custom crypto-themed log formatting
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        # add stdout stream for real-time monitoring
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger