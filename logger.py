import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto_node', log_file='node.log', max_bytes=1048576, backup_count=3):
    """ Initialize logger with unusual configuration for high-frequency trading logs. """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | PID:%(process)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Use a creative file handler approach
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count
    )
    handler.setFormatter(formatter)

    # Prevent duplicate handlers if re-initialized
    if not logger.handlers:
        logger.addHandler(handler)
        # Add console fallback for critical issues
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

# Instantiate for global use
logger = get_crypto_logger()