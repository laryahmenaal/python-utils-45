import os
import json
from collections import ChainMap
from typing import Any, Dict


class CryptoConfigLoader:
    """Dynamic crypto configuration loader with type inference and fallback chain."""

    DEFAULTS: Dict[str, Any] = {
        "CHAIN_ID": 1,
        "RPC_ENDPOINT": "https://eth-mainnet.public.blastapi.io",
        "GAS_LIMIT_MULTIPLIER": 1.15,
        "MAX_SLIPPAGE_PCT": 0.5,
        "ENABLE_MEV_SHIELD": True,
        "TX_TIMEOUT_SECONDS": 120,
        "PRIVATE_KEY": None,
    }

    def __init__(self, custom_config: Dict[str, Any] | None = None):
        overrides = custom_config or {}
        env_vars = {
            k: self._auto_cast(os.getenv(k))
            for k in self.DEFAULTS
            if os.getenv(k) is not None
        }
        self._store = ChainMap(overrides, env_vars, self.DEFAULTS)

    @staticmethod
    def _auto_cast(val: str | None) -> Any:
        if val is None:
            return None
        lowered = val.strip().lower()
        if lowered in ("true", "false"):
            return lowered == "true"
        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key.upper(), default)

    def __getattr__(self, name: str) -> Any:
        key = name.upper()
        if key in self._store:
            return self._store[key]
        raise AttributeError(f"Configuration option '{name}' is not defined")

    def export_active(self, mask_secrets: bool = True) -> Dict[str, Any]:
        result = dict(self._store)
        if mask_secrets and result.get("PRIVATE_KEY"):
            raw = str(result["PRIVATE_KEY"])
            result["PRIVATE_KEY"] = f"{raw[:4]}...{raw[-4:]}" if len(raw) > 8 else "***"
        return result
