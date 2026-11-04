import json
import os
from typing import Any, Dict

class ConfigLoader:
    """cryptographic configuration loader with recursive default merging"""
    def __init__(self, defaults: Dict[str, Any]):
        self._conf = defaults

    def load(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return self._conf
        with open(path, 'r') as f:
            user_data = json.load(f)
        return self._deep_merge(self._conf, user_data)

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

# usage for crypto modules
DEFAULT_SETTINGS = {
    "cipher": "AES-256-GCM",
    "keys": {
        "rotation": True,
        "length": 32
    },
    "network": {
        "nodes": ["localhost:8080"]
    }
}

loader = ConfigLoader(DEFAULT_SETTINGS)
active_config = loader.load("config.json")