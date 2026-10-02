import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with fallback defaults."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, file_path: str) -> None:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    loaded = json.load(f)
                    self._data.update({k: v for k, v in loaded.items() if k in self._data})
        except (json.JSONDecodeError, OSError):
            pass

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    @property
    def raw(self) -> Dict[str, Any]:
        return self._data

def get_crypto_config() -> ConfigLoader:
    defaults = {
        "rpc_url": "https://mainnet.infura.io",
        "timeout": 30,
        "retries": 3,
        "verify_ssl": True
    }
    loader = ConfigLoader(defaults)
    loader.load("config.json")
    return loader