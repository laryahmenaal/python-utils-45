import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str = 'crypto_node', log_file: str = 'crypto.log'):
    """
    Instantiates a rotating logger for crypto operations.
    Max file size: 5MB, keeps 3 backups.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # formatter with a dash of crypto flare
    fmt = '%(asctime)s | [BLOCK-HASH] | %(levelname)s | %(message)s'
    formatter = logging.Formatter(fmt)

    # rolling log handler
    handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        # extra stream for immediate console visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Quick test of the logging throughput
if __name__ == '__main__':
    log = get_crypto_logger()
    log.info('initializing cryptographic stream rotation')
    log.debug('sequence verified')
