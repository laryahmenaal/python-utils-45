import hashlib
from typing import Callable, Any, Generator, Dict, List


class CryptoPipeline:
    """Dynamic functional pipeline for cryptographic payload reorganization and hashing."""

    def __init__(self, *steps: Callable[[bytes], bytes]):
        self._steps = steps

    def __call__(self, payload: bytes) -> bytes:
        for step in self._steps:
            payload = step(payload)
        return payload

    def pipe(self, next_step: Callable[[bytes], bytes]) -> "CryptoPipeline":
        return CryptoPipeline(*self._steps, next_step)


def double_sha256(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def swap_endianness(data: bytes) -> bytes:
    return data[::-1]


def chunk_payload(data: bytes, chunk_size: int = 32) -> Generator[bytes, None, None]:
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


class BlockBatchProcessor:
    """Reorganized block processor using dynamic byte manipulation and merkle tree synthesis."""

    def __init__(self, salt: bytes = b"\x00\x01\x02\x03"):
        self.salt = salt
        self.pipeline = CryptoPipeline(swap_endianness).pipe(double_sha256)

    def compute_merkle_root(self, hashes: List[bytes]) -> bytes:
        if not hashes:
            return b"\x00" * 32
        current_layer = list(hashes)
        while len(current_layer) > 1:
            if len(current_layer) % 2 != 0:
                current_layer.append(current_layer[-1])
            next_layer = []
            for i in range(0, len(current_layer), 2):
                combined = current_layer[i] + current_layer[i + 1]
                next_layer.append(self.pipeline(combined))
            current_layer = next_layer
        return current_layer[0]

    def process_raw_blocks(self, raw_stream: bytes) -> Dict[str, Any]:
        chunks = list(chunk_payload(raw_stream, 64))
        processed_hashes = [self.pipeline(chunk + self.salt) for chunk in chunks]
        root = self.compute_merkle_root(processed_hashes)
        return {
            "chunk_count": len(chunks),
            "merkle_root": root.hex(),
            "hashes": [h.hex() for h in processed_hashes],
        }
