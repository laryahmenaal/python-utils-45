import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "CRYPTO_"):
        self._config = defaults.copy()
        self._env_prefix = env_prefix

    def load_from_file(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, "r") as f:
                self._config.update(json.load(f))
        self._apply_env_overrides()

    def _apply_env_overrides(self) -> None:
        for key in self._config.keys():
            env_val = os.environ.get(f"{self._env_prefix}{key.upper()}")
            if env_val is not None:
                try:
                    self._config[key] = json.loads(env_val)
                except json.JSONDecodeError:
                    self._config[key] = env_val

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def __repr__(self) -> str:
        return f"ConfigLoader(keys={list(self._config.keys())})"