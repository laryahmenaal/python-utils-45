import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = 'crypto_node', path: str = 'logs/node.log') -> logging.Logger:
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [TX-ID:%(process)d] | %(message)s'
        )

        # Rotates at 5MB, keeps 3 backups
        handler = RotatingFileHandler(
            path, maxBytes=5*1024*1024, backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Console output for real-time crypto monitoring
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Instantiate singleton for global usage
node_logger = get_crypto_logger()