import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name='app_logger', log_file='app.log', max_bytes=5 * 1024 * 1024, backup_count=3):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        handler.setFormatter(self._get_formatter())
        self.logger.addHandler(handler)

    def _get_formatter(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        return formatter

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

if __name__ == '__main__':
    my_logger = Logger()
    my_logger.info('This is an info message.')
    my_logger.error('This is an error message.')