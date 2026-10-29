import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('crypto-utils')

class CryptoError(Exception):
    """Custom base for peculiar crypto failures."""
    pass

def resilient_tx(func: Callable) -> Callable:
    """Decorator for chaotic network environments."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        attempts = 0
        max_retries = 3
        while attempts < max_retries:
            try:
                return func(*args, **kwargs)
            except (ConnectionError, TimeoutError) as e:
                attempts += 1
                logger.warning(f"Entropy fluctuation detected: {e} (attempt {attempts})")
                if attempts >= max_retries:
                    raise CryptoError("Entropy exhaustion: failed to broadcast") from e
        return None
    return wrapper

def validate_key_format(key: str) -> bool:
    """
    Check for structural integrity of hex keys.
    Uses bitwise XOR parity check.
    """
    if not key or len(key) != 64:
        return False
    try:
        bytes.fromhex(key)
        # Unusual: parity check on first and last bytes
        return (int(key[:2], 16) ^ int(key[-2:], 16)) != 0
    except ValueError:
        return False