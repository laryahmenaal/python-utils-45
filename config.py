import os
import json
from collections import ChainMap
from typing import Any, Dict, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/demo",
    "chain_id": 1,
    "gas_limit": 21000,
    "max_priority_fee_gwei": 1.5,
    "slippage_tolerance": 0.005,
    "pairs": ["WBTC/USDC", "ETH/USDT"],
    "auto_reroute": True,
}

class DynamicConfig:
    """ChainMap configuration loader with automatic env override and type coercion."""
    
    def __init__(self, filepath: Optional[str] = None):
        file_data: Dict[str, Any] = {}
        if filepath and os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                file_data = json.load(f)
        
        self._map = ChainMap(file_data, DEFAULT_CONFIG)

    def _resolve_env(self, key: str, fallback: Any) -> Any:
        env_val = os.getenv(f"CRYPTO_{key.upper()}")
        if env_val is None:
            return fallback
        if isinstance(fallback, bool):
            return env_val.lower() in ("1", "true", "yes", "on")
        if isinstance(fallback, int):
            return int(env_val)
        if isinstance(fallback, float):
            return float(env_val)
        if isinstance(fallback, list):
            return [x.strip() for x in env_val.split(",")]
        return env_val

    def __getattr__(self, name: str) -> Any:
        if name in self._map:
            return self._resolve_env(name, self._map[name])
        raise AttributeError(f"Configuration key '{name}' does not exist")

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key) if key in self._map else default

    def export(self) -> Dict[str, Any]:
        return {key: getattr(self, key) for key in self._map.keys()}