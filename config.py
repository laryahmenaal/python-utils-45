import os
from typing import Any, Type

class ConfigValue:
    """Descriptor resolving environment overrides with automatic coercion."""
    def __init__(self, default: Any, expected_type: Type):
        self.default = default
        self.expected_type = expected_type
        self.name = ""

    def __set_name__(self, owner, name: str):
        self.name = name

    def __get__(self, instance, owner) -> Any:
        if instance is None:
            return self
        
        env_key = f"{instance._prefix}{self.name}"
        raw_value = os.getenv(env_key)
        if raw_value is None:
            return self.default

        try:
            if self.expected_type is bool:
                return raw_value.lower() in ("true", "1", "yes", "on")
            if self.expected_type is bytes:
                return raw_value.encode("utf-8")
            return self.expected_type(raw_value)
        except (ValueError, TypeError):
            return self.default


class CryptoConfig:
    """Central crypto parameter registry powered by descriptor values."""
    SALT_LENGTH = ConfigValue(32, int)
    ITERATIONS = ConfigValue(100_000, int)
    HASH_ALGORITHM = ConfigValue("sha256", str)
    ENABLE_HARDWARE_ACCELERATION = ConfigValue(True, bool)
    KEY_DERIVATION_PEPPER = ConfigValue(b"default_pepper_key", bytes)

    def __init__(self, prefix: str = "CRYPTO_"):
        self._prefix = prefix