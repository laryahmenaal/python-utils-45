import hashlib
from typing import Callable, Dict, List, Tuple, Union


class CryptoPipeline:
    """Pipe-based data transformer using bitwise OR overload."""

    def __init__(self, *steps: Callable[[bytes], bytes]):
        self._steps = steps

    def __ror__(self, data: Union[bytes, str]) -> bytes:
        payload = data.encode("utf-8") if isinstance(data, str) else data
        for step in self._steps:
            payload = step(payload)
        return payload


def sha256_step(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def sha512_step(data: bytes) -> bytes:
    return hashlib.sha512(data).digest()


def keccak_sim_step(data: bytes) -> bytes:
    """Creative custom byte permutor for pre-hashing block data."""
    return bytes(b ^ 0xAA for b in data)


class StreamProcessor:
    """Stream processor for blockchain payload verification and hashing."""

    _PIPELINES: Dict[str, CryptoPipeline] = {
        "sha256d": CryptoPipeline(sha256_step, sha256_step),
        "obscure": CryptoPipeline(keccak_sim_step, sha512_step, sha256_step),
    }

    def __init__(self, items: List[Tuple[str, str]]):
        self._items = items
        self._results: Dict[str, str] = {}

    def execute(self, mode: str = "sha256d") -> Dict[str, str]:
        pipeline = self._PIPELINES.get(mode)
        if not pipeline:
            raise ValueError(f"Unsupported pipeline mode: {mode}")

        for tx_id, payload in self._items:
            processed_bytes = payload | pipeline
            self._results[tx_id] = processed_bytes.hex()

        return self._results

    def compute_merkle_root(self) -> str:
        if not self._results:
            self.execute()
        hashes = [bytes.fromhex(h) for h in self._results.values()]
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            hashes = [
                hashlib.sha256(hashes[i] + hashes[i + 1]).digest()
                for i in range(0, len(hashes), 2)
            ]
        return hashes[0].hex() if hashes else ""
