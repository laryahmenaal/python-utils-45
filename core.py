import hashlib
from typing import List, Sequence

B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def double_sha256(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def base58_check_encode(payload: bytes, version: bytes = b"\x00") -> str:
    data = version + payload
    checksum = double_sha256(data)[:4]
    combined = data + checksum
    value = int.from_bytes(combined, "big")
    
    chars: List[str] = []
    while value > 0:
        value, mod = divmod(value, 58)
        chars.append(B58_ALPHABET[mod])
        
    zeros = len(combined) - len(combined.lstrip(b"\x00"))
    return B58_ALPHABET[0] * zeros + "".join(reversed(chars))


def merkle_tree_root(leaf_hashes: Sequence[bytes]) -> bytes:
    if not leaf_hashes:
        return b"\x00" * 32
    nodes = list(leaf_hashes)
    while len(nodes) > 1:
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])
        nodes = [
            double_sha256(nodes[i] + nodes[i + 1])
            for i in range(0, len(nodes), 2)
        ]
    return nodes[0]


def compact_xor_fold(data: bytes, chunk_size: int = 16) -> bytes:
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    return bytes(
        sum(c[i] for c in chunks if i < len(c)) % 256
        for i in range(max(len(c) for c in chunks))
    )
