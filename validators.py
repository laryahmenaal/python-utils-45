import hashlib
from typing import Callable, Dict


class ValidationMatrix:
    """Multi-chain address and hash validation pipeline."""

    B58_CHARS = set("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")

    @staticmethod
    def _eip55_checksum(addr_str: str) -> str:
        clean = addr_str.lower().replace("0x", "")
        hashed = hashlib.sha3_256(clean.encode("ascii")).hexdigest()
        return "0x" + "".join(
            c.upper() if int(hashed[i], 16) >= 8 else c
            for i, c in enumerate(clean)
        )

    @classmethod
    def is_checksum_eth_address(cls, address: str) -> bool:
        if not isinstance(address, str) or len(address) != 42 or not address.startswith("0x"):
            return False
        if not all(c in "0123456789abcdefABCDEF" for c in address[2:]):
            return False
        return cls._eip55_checksum(address) == address

    @classmethod
    def is_base58_solana(cls, address: str) -> bool:
        if not isinstance(address, str) or not (32 <= len(address) <= 44):
            return False
        return set(address).issubset(cls.B58_CHARS)

    @classmethod
    def validate_payload(cls, chain: str, payload: str, kind: str = "address") -> bool:
        chain_map: Dict[str, Dict[str, Callable[[str], bool]]] = {
            "ethereum": {
                "address": cls.is_checksum_eth_address,
                "tx": lambda x: isinstance(x, str) and len(x) == 66 and x.startswith("0x"),
            },
            "solana": {
                "address": cls.is_base58_solana,
                "tx": cls.is_base58_solana,
            },
        }
        validator = chain_map.get(chain.lower(), {}).get(kind.lower())
        return validator(payload) if validator else False


def quick_check(chain: str, payload: str) -> bool:
    """Convenience wrapper for single-call validation dispatch."""
    return ValidationMatrix.validate_payload(chain, payload)
