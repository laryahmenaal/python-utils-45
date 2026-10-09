import hashlib
import hmac
from typing import Callable, Iterable, Any, Generator


class CryptoPipe:
    """Composable pipeline transformer for cryptographic stream processing."""

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func

    def __ror__(self, other: Any) -> Any:
        if isinstance(other, Iterable) and not isinstance(other, (str, bytes, dict)):
            return (self.func(item) for item in other)
        return self.func(other)

    def __or__(self, next_pipe: "CryptoPipe") -> "CryptoPipe":
        return CryptoPipe(lambda x: next_pipe.func(self.func(x)))


class CryptoStreamProcessor:
    """Stream processor offering reusable pipeline transformations for transaction data."""

    @staticmethod
    def sha256_digest() -> CryptoPipe:
        return CryptoPipe(
            lambda data: hashlib.sha256(
                data.encode("utf-8") if isinstance(data, str) else data
            ).hexdigest()
        )

    @staticmethod
    def double_sha256() -> CryptoPipe:
        return CryptoPipe(
            lambda data: hashlib.sha256(
                hashlib.sha256(
                    data.encode("utf-8") if isinstance(data, str) else data
                ).digest()
            ).hexdigest()
        )

    @staticmethod
    def hmac_sign(secret_key: bytes) -> CryptoPipe:
        return CryptoPipe(
            lambda data: hmac.new(
                secret_key,
                data.encode("utf-8") if isinstance(data, str) else data,
                hashlib.sha256,
            ).hexdigest()
        )

    @classmethod
    def process_batch(
        cls, records: Iterable[str], secret_key: bytes
    ) -> Generator[dict[str, str], None, None]:
        pipeline = cls.double_sha256() | cls.hmac_sign(secret_key)
        for item in records:
            yield {
                "payload": item,
                "checksum": item | cls.sha256_digest(),
                "signature": pipeline.func(item),
            }
