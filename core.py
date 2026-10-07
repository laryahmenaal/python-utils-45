import hashlib
import struct
from typing import List


class FastBatchHasher:
    """High-performance zero-copy batch hasher for crypto transaction streams."""

    __slots__ = ("_chunk_size", "_cache", "_hash_ring")

    def __init__(self, chunk_size: int = 64):
        self._chunk_size = chunk_size
        self._cache = {}
        self._hash_ring = bytearray(chunk_size * 256)

    def process_stream(self, raw_bytes: bytes) -> List[bytes]:
        """Process raw transaction payload using memoryview slices and header lookup."""
        hashes = []
        mv = memoryview(raw_bytes)
        step = self._chunk_size
        limit = len(mv) - (len(mv) % step)

        for offset in range(0, limit, step):
            chunk = mv[offset : offset + step]
            header_sig = struct.unpack_from("<Q", chunk, 0)[0]

            cached_hash = self._cache.get(header_sig)
            if cached_hash is not None:
                hashes.append(cached_hash)
                continue

            digest = hashlib.sha256(hashlib.sha256(chunk).digest()).digest()
            if len(self._cache) > 4096:
                self._cache.clear()
            self._cache[header_sig] = digest
            hashes.append(digest)

        return hashes

    def bitwise_stream_checksum(self, payloads: List[bytes]) -> int:
        """Fast bitwise XOR checksum aggregator using uint64 memory slices."""
        acc = 0
        for payload in payloads:
            mv = memoryview(payload)
            limit = len(mv) - (len(mv) % 8)
            for i in range(0, limit, 8):
                acc ^= struct.unpack_from("<Q", mv, i)[0]
        return acc
