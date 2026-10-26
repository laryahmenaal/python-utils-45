import math
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Tuple, Union


class CryptoDataAnomaly(Exception):
    """Base exception for anomalous crypto market data."""
    pass


class PrecisionError(CryptoDataAnomaly):
    """Raised when satoshi precision or boundary checks fail."""
    pass


class IntegrityError(CryptoDataAnomaly):
    """Raised on corrupt orderbook snapshots or invalid spreads."""
    pass


def resilient_parse(fallback_value: Any = None):
    """Decorator catching edge-case math/type anomalies in market payloads."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (InvalidOperation, TypeError, ValueError, ZeroDivisionError) as err:
                if isinstance(fallback_value, dict):
                    return {**fallback_value, "_error_recovered": str(err)}
                return fallback_value
        return wrapper
    return decorator


class OrderBookEdgeProcessor:
    """Processes volatile orderbook deltas with strict boundary checks."""

    MAX_SATOSHI = Decimal("2100000000000000")
    MIN_PRICE_TICK = Decimal("0.00000001")

    @classmethod
    @resilient_parse(fallback_value={"bids": [], "asks": [], "valid": False})
    def sanitize_depth_delta(
        cls, raw_bids: List[Any], raw_asks: List[Any]
    ) -> Dict[str, Union[List[Tuple[Decimal, Decimal]], bool]]:
        sanitized_bids = cls._filter_levels(raw_bids, reverse=True)
        sanitized_asks = cls._filter_levels(raw_asks, reverse=False)

        if sanitized_bids and sanitized_asks:
            highest_bid = sanitized_bids[0][0]
            lowest_ask = sanitized_asks[0][0]
            if highest_bid >= lowest_ask:
                raise IntegrityError(f"Crossed orderbook detected: Bid {highest_bid} >= Ask {lowest_ask}")

        return {"bids": sanitized_bids, "asks": sanitized_asks, "valid": True}

    @classmethod
    def _filter_levels(cls, levels: List[Any], reverse: bool) -> List[Tuple[Decimal, Decimal]]:
        valid_levels = []
        for item in levels:
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue
            try:
                price = Decimal(str(item[0]))
                qty = Decimal(str(item[1]))
            except (InvalidOperation, TypeError):
                continue

            if price.is_nan() or price.is_infinite() or qty.is_nan() or qty.is_infinite():
                continue
            if price < cls.MIN_PRICE_TICK or qty <= Decimal("0"):
                continue
            if qty > cls.MAX_SATOSHI:
                raise PrecisionError(f"Unrealistic quantity anomaly: {qty}")

            valid_levels.append((price, qty))

        return sorted(valid_levels, key=lambda x: x[0], reverse=reverse)
