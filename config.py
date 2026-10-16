import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader using a layered override pattern."""
    def __init__(self, defaults: Dict[str, Any]):
        self._config = defaults

    def load_from_env(self, prefix: str = "CRYPTO_") -> None:
        for key in self._config:
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val is not None:
                self._config[key] = self._parse_val(env_val)

    def _parse_val(self, val: str) -> Any:
        if val.lower() in ('true', 'false'): return val.lower() == 'true'
        try: return int(val)
        except ValueError: return val

    def __getitem__(self, key: str) -> Any:
        return self._config.get(key)

    def patch(self, overrides: Dict[str, Any]) -> None:
        self._config.update(overrides)

def get_crypto_config() -> ConfigLoader:
    defaults = {
        "node_url": "wss://mainnet.infura.io/ws/v3/",
        "timeout": 30,
        "verify_ssl": True,
        "retry_limit": 3
    }
    loader = ConfigLoader(defaults)
    loader.load_from_env()
    return loader