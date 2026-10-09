import os
import base64
from typing import Any, Dict, get_type_hints

class CryptoConfig:
    """Dynamic configuration loader with automatic base64 decoding and environment overrides."""
    
    API_URL: str = "https://api.binance.com"
    RETRY_LIMIT: int = 3
    ENCRYPTION_KEY_B64: bytes = b"ZGVmYXVsdF9rZXlfMzJfYnl0ZXNfX19fX19fX19fXw=="
    USE_SANDBOX: bool = False

    def __init__(self, overrides: Dict[str, Any] = None):
        self._values = overrides or {}
        self._resolved_cache = {}

    def __getattr__(self, name: str) -> Any:
        if name in self._resolved_cache:
            return self._resolved_cache[name]

        annotations = get_type_hints(self.__class__)
        if name not in annotations and not hasattr(self.__class__, name):
            raise AttributeError(f"Configuration key '{name}' is not defined")

        expected_type = annotations.get(name, str)
        val = self._values.get(name, os.environ.get(name, getattr(self.__class__, name, None)))
        
        resolved = self._coerce(val, expected_type, name)
        self._resolved_cache[name] = resolved
        return resolved

    def _coerce(self, value: Any, target_type: type, name: str) -> Any:
        if isinstance(value, str):
            if target_type is bytes and name.endswith("_B64"):
                return base64.b64decode(value.encode("utf-8"))
            if target_type is bool:
                return value.lower() in ("true", "1", "t", "yes")
        try:
            return target_type(value)
        except (ValueError, TypeError):
            return value

    def __repr__(self) -> str:
        safe_dict = {}
        for key in get_type_hints(self.__class__):
            val = getattr(self, key)
            if "KEY" in key or "SECRET" in key:
                safe_dict[key] = "***MASKED***"
            else:
                safe_dict[key] = val
        return f"CryptoConfig({safe_dict})"