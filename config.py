import os
import json
from typing import Any, Dict, Optional

DEFAULT_CRYPTO_CONFIG: Dict[str, Any] = {
    "network": "mainnet",
    "rpc_nodes": {
        "mainnet": "https://eth-mainnet.g.alchemy.com/v2/demo",
        "testnet": "https://eth-goerli.g.alchemy.com/v2/demo",
    },
    "trading": {
        "max_slippage_pct": 0.5,
        "gas_limit_multiplier": 1.15,
        "default_gas_price_gwei": 25.0,
        "auto_approve_tokens": False,
    },
    "security": {
        "min_confirmations": 12,
        "enforce_checksum": True,
    }
}

class ConfigLoader:
    """Dynamic configuration loader with environment overlay and fallback defaults."""

    def __init__(self, config_path: Optional[str] = None):
        self._config = json.loads(json.dumps(DEFAULT_CRYPTO_CONFIG))
        if config_path and os.path.exists(config_path):
            self._load_file(config_path)
        self._apply_env_overrides()

    def _load_file(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
            self._merge(self._config, user_cfg)

    def _merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        for key, val in update.items():
            if isinstance(val, dict) and key in base and isinstance(base[key], dict):
                self._merge(base[key], val)
            else:
                base[key] = val

    def _apply_env_overrides(self) -> None:
        prefix = "CRYPTO_CFG_"
        for env_key, value in os.environ.items():
            if env_key.startswith(prefix):
                parts = env_key[len(prefix):].lower().split("_")
                self._set_nested(self._config, parts, value)

    def _set_nested(self, target: Dict[str, Any], path: list, value: str) -> None:
        curr = target
        for part in path[:-1]:
            if part not in curr or not isinstance(curr[part], dict):
                curr[part] = {}
            curr = curr[part]
        leaf = path[-1]
        if value.lower() in ("true", "false"):
            curr[leaf] = value.lower() == "true"
        else:
            try:
                curr[leaf] = int(value) if value.isdigit() else float(value)
            except ValueError:
                curr[leaf] = value

    def get(self, path: str, default: Any = None) -> Any:
        keys = path.split(".")
        curr = self._config
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            else:
                return default
        return curr

    def __getitem__(self, item: str) -> Any:
        return self.get(item)

    def __repr__(self) -> str:
        return f"ConfigLoader(network='{self.get('network')}')"
