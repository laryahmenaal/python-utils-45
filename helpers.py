import json
import hashlib
from decimal import Decimal, getcontext
from collections import Counter
from typing import Dict, Any, List, Optional
getcontext().prec = 28

def handle_crypto_data(raw_input: str) -> Dict[str, Any]:
    try:
        parsed = json.loads(raw_input)
    except (json.JSONDecodeError, TypeError, ValueError):
        parsed = {"crypto_data": []}

    crypto_items: List[Dict[str, Any]] = parsed.get("crypto_data", parsed.get("items", []))

    hash_counter = Counter()
    total_value = Decimal("0")
    for item in crypto_items:
        if not isinstance(item, dict):
            continue
        coin = str(item.get("coin", "unknown")).lower().strip()
        amount_str = str(item.get("amount", "0"))
        try:
            amount = Decimal(amount_str)
        except (ValueError, TypeError):
            amount = Decimal("0")
        sig_input = f"{coin}{amount.normalize()}"
        unique_sig = hashlib.blake2b(sig_input.encode(), digest_size=6).hexdigest()
        hash_counter[unique_sig] += 1
        total_value += amount

    xor_fingerprint = 0
    for sig in hash_counter:
        try:
            xor_fingerprint ^= int(sig, 16)
        except ValueError:
            continue

    formatted_total = str(total_value.quantize(Decimal("0.00000001")))
    return {
        "unique_signatures": dict(hash_counter),
        "aggregated_value": formatted_total,
        "fingerprint": hex(xor_fingerprint)[2:],
        "count": len(crypto_items)
    }

def format_crypto_amount(amount: str, precision: int = 8) -> str:
    try:
        d = Decimal(amount)
        exp = Decimal("1e-" + str(precision))
        formatted = d.quantize(exp)
        return str(formatted)
    except (ValueError, TypeError, ArithmeticError):
        return "0." + "0" * precision

def derive_crypto_key(seed: str, iterations: int = 3) -> str:
    if not seed:
        seed = "default_crypto_seed"
    key = seed.encode("utf-8")
    for i in range(iterations):
        key = hashlib.sha3_256(key + str(i).encode()).digest()
    return key.hex()[:64]