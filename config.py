import os
import json
from typing import Any, Dict

class CryptoConfig:
    """Dynamic configuration loader with default-fallback type casting.

    Prioritizes: Environment (CRYPTO_*) > config.json > Defaults
    """
    DEFAULTS: Dict[str, Any] = {
        "RPC_URL": "https://localhost:8545",
        "GAS_LIMIT": 21000,
        "PRIVATE_KEY": "",
        "NETWORK_ID": 1,
        "STRICT_MODE": True,
    }

    def __init__(self, filepath: str = "config.json"):
        self._config: Dict[str, Any] = {}
        self._load(filepath)

    def _load(self, filepath: str) -> None:
        merged = self.DEFAULTS.copy()
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    file_data = json.load(f)
                    merged.update({k.upper(): v for k, v in file_data.items()})
            except (json.JSONDecodeError, OSError):
                pass

        for key, default_val in self.DEFAULTS.items():
            env_key = f"CRYPTO_{key}"
            env_val = os.environ.get(env_key)
            if env_val is not None:
                val_type = type(default_val)
                try:
                    if val_type is bool:
                        merged[key] = env_val.lower() in ("true", "1", "yes")
                    else:
                        merged[key] = val_type(env_val)
                except ValueError:
                    merged[key] = env_val

        self._config = merged

    def __getattr__(self, name: str) -> Any:
        upper_name = name.upper()
        if upper_name in self._config:
            return self._config[upper_name]
        raise AttributeError(f"Configuration parameter '{name}' is not defined")

    def __repr__(self) -> str:
        safe_config = {
            k: ("*" * 8 if "KEY" in k and v else v)
            for k, v in self._config.items()
        }
        return f"CryptoConfig({safe_config})"
