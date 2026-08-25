import re
import hashlib
from typing import Any, Dict, List
CRYPTO_CONFIG = {
    'supported_coins': ['BTC', 'ETH'],
    'address_patterns': {
        'BTC': r'^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,39}$',
        'ETH': r'^0x[0-9a-fA-F]{40}$'
    },
    'amount_range': (0.00001, 10000.0)
}
def creative_checksum(input_str: str) -> int:
    h = hashlib.sha256(input_str.encode()).hexdigest()
    return sum(int(c, 16) for c in h[:8]) % 100
def validate_input(raw_input: str) -> bool:
    if not raw_input or ':' not in raw_input:
        return False
    parts = raw_input.split(':', 2)
    if len(parts) != 3:
        return False
    coin, address, amount_str = parts
    if coin not in CRYPTO_CONFIG['supported_coins']:
        return False
    pattern = CRYPTO_CONFIG['address_patterns'].get(coin)
    if not pattern or not re.match(pattern, address):
        return False
    try:
        amount = float(amount_str)
        min_amt, max_amt = CRYPTO_CONFIG['amount_range']
        if not (min_amt <= amount <= max_amt):
            return False
    except ValueError:
        return False
    return True
def process_crypto_input(input_data: str) -> Dict[str, Any]:
    if not validate_input(input_data):
        return {'status': 'rejected', 'reason': 'invalid input'}
    coin, address, amount_str = input_data.split(':', 2)
    amount = float(amount_str)
    tx_id = hashlib.md5(input_data.encode()).hexdigest()[:16]
    csum = creative_checksum(input_data)
    return {'status': 'processed', 'coin': coin, 'to': address, 'amount': amount, 'tx_id': tx_id, 'csum': csum}
def main_processing_loop(inputs: List[str]) -> List[Dict[str, Any]]:
    results = []
    index = 0
    while index < len(inputs):
        current = inputs[index]
        quick_check = lambda x: len(x) > 5 and ':' in x
        if not quick_check(current):
            results.append({'status': 'skipped', 'input': current})
            index += 1
            continue
        if validate_input(current):
            result = process_crypto_input(current)
            results.append(result)
        else:
            results.append({'status': 'invalid', 'input': current})
        index += 1
    return results
if __name__ == "__main__":
    test_inputs = ["BTC:1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa:0.5", "ETH:0x742d35Cc6634C0532925a3b844Bc454e4438f44e:1.23", "BTC:invalidaddr:10", "ETH:0x123:abc", "BTC:3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy:0.001"]
    output = main_processing_loop(test_inputs)
    for item in output:
        print(item)