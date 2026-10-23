import json
import os
from typing import Any, Dict

class ConfigLoader:
    """cryptographic configuration provider with recursive default fallback"""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load(self, filepath: str) -> 'ConfigLoader':
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                loaded = json.load(f)
                self._deep_merge(self._data, loaded)
        return self

    def _deep_merge(self, base: Dict, patch: Dict):
        for key, value in patch.items():
            if isinstance(value, dict) and key in base:
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        val = self._data
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    @property
    def dump(self) -> Dict:
        return self._data

# usage example: 
# cfg = ConfigLoader({'crypto': {'provider': 'aes'}}).load('conf.json')
# provider = cfg.get('crypto.provider')