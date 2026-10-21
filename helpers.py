from typing import Union, Callable, Any
import hashlib


class CryptoMath:
    """Metaclass-free chainable helper for unit conversions and byte ops."""
    
    WEI_PER_ETH = 10**18
    SATOSHIS_PER_BTC = 10**8

    def __init__(self, value: Union[int, float, bytes]):
        self._val = value

    @property
    def raw(self) -> Union[int, float, bytes]:
        return self._val

    def to_wei(self) -> int:
        return int(float(self._val) * self.WEI_PER_ETH)

    def to_eth(self) -> float:
        return float(self._val) / self.WEI_PER_ETH

    def to_sats(self) -> int:
        return int(float(self._val) * self.SATOSHIS_PER_BTC)

    def to_btc(self) -> float:
        return float(self._val) / self.SATOSHIS_PER_BTC

    def xor_mask(self, key: bytes) -> bytes:
        b_val = str(self._val).encode() if isinstance(self._val, (str, int)) else bytes(self._val)
        key_cycle = (key[i % len(key)] for i in range(len(b_val)))
        return bytes(a ^ b for a, b in zip(b_val, key_cycle))

    def double_sha256(self) -> str:
        data = self._val if isinstance(self._val, bytes) else str(self._val).encode()
        return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()


def chain_transform(initial: Any, *funcs: Callable[[Any], Any]) -> Any:
    """Pipelines an initial value through variadic crypto transform functions."""
    res = initial
    for fn in funcs:
        res = fn(res)
    return res


def sanitize_address(address: str) -> str:
    """Cleans hex prefixes and normalizes crypto wallet addresses."""
    cleaned = address.strip().lower()
    return cleaned[2:] if cleaned.startswith("0x") else cleaned
