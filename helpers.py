import math
from typing import Any, Callable, TypeVar, Optional, Union

T = TypeVar("T")

class CryptoEdgeError(Exception):
    """Base exception for crypto-specific boundary violations."""
    pass

class OverflowSatoshisError(CryptoEdgeError):
    pass

def crypto_edge_guard(fallback: Any = None) -> Callable:
    """Decorator catching crypto numerical & encoding edge cases with resilience."""
    def decorator(func: Callable[..., T]) -> Callable[..., Union[T, Any]]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                for arg in list(args) + list(kwargs.values()):
                    if isinstance(arg, float) and (math.isnan(arg) or math.isinf(arg)):
                        raise CryptoEdgeError(f"Non-finite float value detected: {arg}")
                    if isinstance(arg, int) and (arg < 0 or arg > 2**256 - 1):
                        raise OverflowSatoshisError(f"Integer out of 256-bit bounds: {arg}")

                result = func(*args, **kwargs)

                if isinstance(result, float) and math.isnan(result):
                    raise CryptoEdgeError("Computation resulted in NaN")

                return result
            except (ValueError, TypeError, ZeroDivisionError, CryptoEdgeError) as err:
                if fallback is not None:
                    return fallback() if callable(fallback) else fallback
                if isinstance(err, ValueError) and "non-hexadecimal" in str(err):
                    raw_str = args[0] if args and isinstance(args[0], str) else ""
                    cleaned = "".join(c for c in raw_str if c in "0123456789abcdefABCDEF")
                    if len(cleaned) % 2 != 0:
                        cleaned = "0" + cleaned
                    try:
                        return bytes.fromhex(cleaned)
                    except ValueError:
                        pass
                raise CryptoEdgeError(f"Edge case handling failed for {func.__name__}: {err}") from err
        return wrapper
    return decorator

@crypto_edge_guard(fallback=b"\x00" * 32)
def parse_raw_hash(hex_str: str) -> bytes:
    """Parse raw transaction or block hash with resilience against common hex errors."""
    if not hex_str:
        raise CryptoEdgeError("Empty hash string provided")
    if hex_str.startswith("0x") or hex_str.startswith("0X"):
        hex_str = hex_str[2:]
    return bytes.fromhex(hex_str)

@crypto_edge_guard(fallback=0)
def safe_satoshi_conversion(amount: Union[int, float], decimals: int = 8) -> int:
    """Convert float token balance to base units preventing float underflow/overflow."""
    if decimals < 0 or decimals > 18:
        raise CryptoEdgeError(f"Unsupported decimal scale: {decimals}")
    multiplier = 10 ** decimals
    scaled = amount * multiplier
    if isinstance(scaled, float):
        if scaled.is_integer():
            return int(scaled)
        raise CryptoEdgeError(f"Fractional base units remaining after scaling: {scaled}")
    return scaled