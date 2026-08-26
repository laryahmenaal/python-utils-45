import os
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "network": "mainnet",
    "rpc_timeout": 30,
    "gas_limit": 21000,
    "auto_nonce": True,
}

class CryptoConfig:
    def __init__(self, overrides: Dict[str, Any] = None) -> None:
        self._config = DEFAULT_CONFIG.copy()
        if overrides:
            self._config.update(overrides)
        self._load_from_env()

    def _load_from_env(self) -> None:
        prefix = "CRYPTO_"
        for key in self._config:
            env_key = f"{prefix}{key.upper() }"
            if env_key in os.environ:
                val = os.environ[env_key]
                if isinstance(self._config[key], int):
                    val = int(val)
                elif isinstance(self._config[key], bool):
                    val = val.lower() in ("true", "1", "yes")
                self._config[key] = val

    def get(self, key: str) -> Any:
        return self._config.get(key)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

def load_config(overrides: Dict[str, Any] = None) -> CryptoConfig:
    return CryptoConfig(overrides)
