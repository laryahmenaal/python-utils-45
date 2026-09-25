import json
import os
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, defaults: Dict[str, Any], path: str = 'config.json'):
        self.path = path
        self.data = defaults
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                try:
                    user_data = json.load(f)
                    self.data.update({k: v for k, v in user_data.items() if k in self.data})
                except json.JSONDecodeError:
                    pass

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __repr__(self) -> str:
        return f"CryptoConfig({self.data})"

def load_config(defaults: Dict[str, Any]) -> CryptoConfig:
    """Factory for config instance with local override logic"""
    return CryptoConfig(defaults)

if __name__ == '__main__':
    # Example usage for crypto service
    settings = load_config({'rpc_url': 'https://mainnet.infura.io', 'timeout': 30})
    print(f"Active node: {settings['rpc_url']}")