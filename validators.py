import re
import hashlib
from typing import Callable, Dict, Tuple


class AddressValidationEngine:
    """Creative dispatch engine for multi-chain crypto address validation."""

    _validators: Dict[str, Callable[[str], bool]] = {}

    @classmethod
    def register(cls, chain: str) -> Callable:
        def decorator(func: Callable[[str], bool]) -> Callable[[str], bool]:
            cls._validators[chain.lower()] = func
            return func
        return decorator

    @classmethod
    def validate(cls, chain: str, address: str) -> Tuple[bool, str]:
        chain_key = chain.lower()
        if chain_key not in cls._validators:
            return False, f"Unsupported chain: {chain}"
        try:
            is_valid = cls._validators[chain_key](address)
            msg = "Valid address format" if is_valid else "Invalid address format"
            return is_valid, msg
        except Exception as err:
            return False, f"Validation error: {err}"


@AddressValidationEngine.register("ethereum")
@AddressValidationEngine.register("evm")
def _validate_evm(address: str) -> bool:
    if not re.match(r"^0x[a-fA-F0-9]{40}$", address):
        return False
    if address.islower() or address.isupper():
        return True
    clean_addr = address[2:].lower()
    hashed = hashlib.sha3_256(clean_addr.encode()).hexdigest()
    for i, char in enumerate(clean_addr):
        if char.isalpha():
            is_upper = int(hashed[i], 16) >= 8
            if (is_upper and address[2 + i].islower()) or (not is_upper and address[2 + i].isupper()):
                return False
    return True


@AddressValidationEngine.register("bitcoin")
def _validate_btc(address: str) -> bool:
    btc_bech32 = r"^(bc1)[0-39-ac-hj-np-z]{8,87}$"
    btc_legacy = r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$"
    return bool(re.match(btc_bech32, address) or re.match(btc_legacy, address))


@AddressValidationEngine.register("solana")
def _validate_sol(address: str) -> bool:
    return bool(re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", address))


def is_valid_crypto_address(chain: str, address: str) -> Tuple[bool, str]:
    """Utility wrapper function to validate crypto address for a specific chain."""
    return AddressValidationEngine.validate(chain, address)
