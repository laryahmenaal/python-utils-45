import json
import os
from collections import ChainMap
from typing import Any, Dict, Union

DEFAULT_CRYPTO_CONFIG: Dict[str, Any] = {
    "network": "mainnet",
    "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/demo",
    "chain_id": 1,
    "gas_multiplier": 1.15,
    "max_slippage_pct": 0.5,
    "retry_attempts": 3,
    "enable_mev_protection": True,
}

class CryptoConfigLoader:
    def __init__(self, filepath: Union[str, None] = None):
        self._raw_file_config = self._load_file(filepath) if filepath else {}
        self._env_config = self._load_env()
        self._combined = ChainMap(self._env_config, self._raw_file_config, DEFAULT_CRYPTO_CONFIG)

    def _load_file(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _load_env(self) -> Dict[str, Any]:
        env_map = {}
        for key in DEFAULT_CRYPTO_CONFIG:
            env_key = f"CRYPTO_{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                default_type = type(DEFAULT_CRYPTO_CONFIG[key])
                try:
                    if default_type == bool:
                        env_map[key] = val.lower() in ("true", "1", "yes")
                    else:
                        env_map[key] = default_type(val)
                except ValueError:
                    env_map[key] = val
        return env_map

    def __getattr__(self, name: str) -> Any:
        if name in self._combined:
            return self._combined[name]
        raise AttributeError(f"Configuration option '{name}' not found")

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._combined)

    def __repr__(self) -> str:
        return f"<CryptoConfig network={self.network!r} chain_id={self.chain_id}>"
