import os
import re
import logging
from logging.handlers import RotatingFileHandler


class CryptoSanitizingFormatter(logging.Formatter):
    """Formatter that automatically redacts sensitive private keys and truncates addresses."""

    PRIVATE_KEY_REGEX = re.compile(r'(?i)(private_?key|secret|seed_phrase)["\s:=]+([a-f0-9]{64})')
    ETH_ADDR_REGEX = re.compile(r'(0x[a-fA-F0-9]{40})')

    def format(self, record: logging.LogRecord) -> str:
        original_msg = super().format(record)
        sanitized = self.PRIVATE_KEY_REGEX.sub(r'\1: [REDACTED_SECURE_KEY]', original_msg)
        sanitized = self.ETH_ADDR_REGEX.sub(
            lambda m: f"{m.group(1)[:6]}...{m.group(1)[-4:]}", 
            sanitized
        )
        return sanitized


def configure_rotating_logger(
    name: str = "crypto_node",
    log_dir: str = "logs",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 7
) -> logging.Logger:
    """Sets up a secure, auto-rotating file and console logger for crypto ops."""
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    file_handler = RotatingFileHandler(
        log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    formatter = CryptoSanitizingFormatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s [ts:%(created)f] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
