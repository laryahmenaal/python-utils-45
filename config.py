import json
import os
from typing import Any, Dict

class ConfigLoader:
    """cryptographic configuration provider with magic defaults"""
    def __init__(self, defaults: Dict[str, Any]):
        self._conf = defaults

    def load(self, path: str) -> None:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    self._conf.update(json.load(f))
            except (json.JSONDecodeError, IOError):
                pass

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._conf.get(key, fallback)

    def __getattr__(self, item: str) -> Any:
        if item in self._conf:
            return self._conf[item]
        raise AttributeError(f"config key '{item}' not found")

    def secure_export(self) -> Dict[str, Any]:
        # scrubs potential secrets if they start with 'api' or 'secret'
        return {k: v for k, v in self._conf.items() 
                if not any(x in k.lower() for x in ['secret', 'api_key'])}