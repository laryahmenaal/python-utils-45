import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = 'CRYPT_'):
        self.config = defaults.copy()
        self.env_prefix = env_prefix

    def load(self, path: str = 'config.json') -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.config.update(json.load(f))
        self._load_env()
        return self

    def _load_env(self):
        for key in self.config.keys():
            env_key = f"{self.env_prefix}{key.upper()}"
            val = os.getenv(env_key)
            if val is not None:
                self.config[key] = type(self.config[key])(val)

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def __repr__(self) -> str:
        return f"ConfigLoader({self.config})"

# Usage pattern for crypto keys
def get_app_config():
    defaults = {
        "api_key": "default_dev_key",
        "node_port": 8545,
        "debug_mode": False
    }
    return ConfigLoader(defaults).load()