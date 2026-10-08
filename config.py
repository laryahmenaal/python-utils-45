import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with chainable fallback logic."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load(self, file_path: str) -> 'ConfigLoader':
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    self._data.update(json.load(f))
                except json.JSONDecodeError:
                    pass
        return self

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Config key {name} not found')

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    @property
    def raw(self) -> Dict[str, Any]:
        return self._data

# Crypto specific default constants
DEFAULT_NETWORK_SETTINGS = {
    'rpc_endpoint': 'https://mainnet.infura.io/v3/',
    'gas_limit': 21000,
    'chain_id': 1
}

settings = ConfigLoader(DEFAULT_NETWORK_SETTINGS).load('user_config.json')