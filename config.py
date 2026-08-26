import os
from typing import Dict, Any

class CryptoConfig:
    __slots__ = ('_settings',)
    
    def __init__(self) -> None:
        self._settings: Dict[str, Any] = {
            "default_cipher": os.getenv("PYUTILS_CIPHER", "AES-GCM-256"),
            "key_derivation_rounds": int(os.getenv("PYUTILS_KDF_ROUNDS", "100000")),
            "entropy_source": os.getenv("PYUTILS_ENTROPY", "/dev/urandom"),
            "digest_algorithm": os.getenv("PYUTILS_DIGEST", "sha3_512"),
            "encoding_scheme": "base58check"
        }
    
    def __getitem__(self, key: str) -> Any:
        if key not in self._settings:
            raise KeyError(f"Configuration key '{key}' does not exist in crypto profile.")
        return self._settings[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        self._settings[key] = value
    
    def export_secure_env(self) -> Dict[str, str]:
        return {k.upper(): str(v) for k, v in self._settings.items() if "key" not k}

config = CryptoConfig()
