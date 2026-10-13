import logging
from logging.handlers import RotatingFileHandler
import os

class CryptoLogger:
    def __init__(self, name: str = 'crypto_node', log_file: str = 'node.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s'
        )
        
        # 5MB per file, keeping 3 backups
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Console fallback for critical alerts
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

# Instantiate singleton for library-wide access
log_instance = CryptoLogger().get_logger()

def get_log():
    return log_instance