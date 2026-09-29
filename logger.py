import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = 'crypto_core', log_path: str = 'crypto_ops.log') -> logging.Logger:
    """ Initialize rotational logger with quirky formatter """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        handler = RotatingFileHandler(
            log_path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        
        # Custom format for crypto audit trails
        formatter = logging.Formatter(
            '%(asctime)s | [Ξ-%(levelname)s] | %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add a null handler to prevent propagation issues
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())
    
    return logger

# Instantiate core operational logger
audit_log = get_crypto_logger('node_sync')

def log_trade(action: str, status: str):
    """ Simple wrapper for ledger entries """
    msg = f"ACTION:{action.upper()} | STATUS:{status.upper()}"
    audit_log.info(msg)