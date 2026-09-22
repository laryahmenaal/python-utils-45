import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str = 'crypto_bot', log_file: str = 'trade_audit.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Creative custom formatter for high-frequency trading context
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d | %(levelname)-7s | %(message)s',
            datefmt='%H:%M:%S'
        )

        # Rotate 5MB logs, keep 3 historical records
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Optional console feedback for local dev
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger

# Singleton pattern instance for module-level import
crypto_logger = get_crypto_logger()