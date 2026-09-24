import json
import os
from typing import Any, Dict

class ConfigLoader:
    """crypto-grade config injection with environment override"""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults
        self._load_from_env()

    def _load_from_env(self) -> None:
        for key in self._data.keys():
            env_val = os.getenv(f"CRYPTO_{key.upper()}")
            if env_val:
                try:
                    self._data[key] = json.loads(env_val)
                except json.JSONDecodeError:
                    self._data[key] = env_val

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __getattr__(self, item: str) -> Any:
        if item in self._data:
            return self._data[item]
        raise AttributeError(f"Config key '{item}' missing")

    @classmethod
    def from_file(cls, path: str, defaults: Dict[str, Any]) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                defaults.update(json.load(f))
        return cls(defaults)

def get_app_config() -> ConfigLoader:
    base = {
        "network": "mainnet",
        "timeout": 30,
        "nodes": ["https://node1.example.com"]
    }
    return ConfigLoader.from_file("settings.json", base)