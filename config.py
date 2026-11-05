import os
import json
from typing import Any, Dict

class ConfigLoader:
    """cryptographic configuration provider using environment overrides"""
    DEFAULTS = {
        "kdf_iterations": 100000,
        "cipher": "AES-256-GCM",
        "key_rotation_days": 30
    }

    def __init__(self, path: str = "config.json"):
        self.path = path
        self._data = self.DEFAULTS.copy()
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        try:
            if os.path.exists(self.path):
                with open(self.path, "r") as f:
                    file_data = json.load(f)
                    self._data.update(file_data)
        except (json.JSONDecodeError, IOError):
            pass
        
        for key in self.DEFAULTS:
            env_val = os.getenv(f"CRYPTO_{key.upper()}")
            if env_val:
                try:
                    self._data[key] = type(self.DEFAULTS[key])(env_val)
                except ValueError:
                    pass

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

config = ConfigLoader()