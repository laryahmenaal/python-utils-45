import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = 'CRYPTO_'):
        self._conf = defaults
        self._prefix = env_prefix

    def load_from_file(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._conf.update(json.load(f))

    def __getattr__(self, name: str) -> Any:
        env_val = os.getenv(f"{self._prefix}{name.upper()}")
        if env_val:
            return self._cast(env_val)
        return self._conf.get(name)

    def _cast(self, val: str) -> Any:
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return val

def get_config(defaults: Dict[str, Any]) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load_from_file('config.json')
    return loader