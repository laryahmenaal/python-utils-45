import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Chain-loading configuration with recursive defaults and env injection."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))
        return self

    def apply_env(self, prefix: str = 'CRYPTO_') -> 'ConfigLoader':
        for key in os.environ:
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                val = os.environ[key]
                try:
                    self._data[clean_key] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    self._data[clean_key] = val
        return self

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    @property
    def settings(self) -> Dict[str, Any]:
        return self._data

# usage: cfg = ConfigLoader({'timeout': 30}).load('conf.json').apply_env()