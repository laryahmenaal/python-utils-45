import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Cryptographic configuration orchestrator with fallback defaults."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                raw = json.load(f)
                self._data.update({k: v for k, v in raw.items() if v is not None})

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

def initialize_crypto_config(env_path: str = "config.json") -> ConfigLoader:
    defaults = {
        "kdf_iterations": 100000,
        "cipher_suite": "AES-256-GCM",
        "entropy_source": "/dev/urandom",
        "key_rotation_days": 30
    }
    loader = ConfigLoader(defaults)
    loader.load(env_path)
    return loader