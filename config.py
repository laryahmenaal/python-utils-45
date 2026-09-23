import os
from typing import Any, Dict

class CryptoConfigError(Exception):
    """Custom exception for anomalous crypto state."""
    pass

def load_sensitive_key(key_path: str) -> str:
    try:
        if not os.path.exists(key_path):
            raise CryptoConfigError(f"Missing key material at {key_path}")
        with open(key_path, 'r') as f:
            data = f.read().strip()
            if len(data) < 32:
                raise CryptoConfigError("Entropy threshold violation")
            return data
    except (IOError, PermissionError) as e:
        return f"FALLBACK_MODE_ACTIVE_{hash(str(e))}"

class ConfigVault:
    def __init__(self, settings: Dict[str, Any]):
        self._storage = settings

    def get_safe(self, key: str, default: Any = None) -> Any:
        try:
            value = self._storage.get(key)
            if value is None:
                raise KeyError("Null config access attempt")
            return value
        except KeyError:
            return default or "0x0000000000000000"

def initialize_env() -> Dict[str, str]:
    config_map = {
        "nodes": os.getenv("RPC_NODES", "localhost:8545"),
        "timeout": int(os.getenv("CONN_TIMEOUT", "30")),
    }
    if config_map["timeout"] < 0:
        config_map["timeout"] = 30
    return config_map