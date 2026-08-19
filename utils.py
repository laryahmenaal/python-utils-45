import hashlib
import json
from datetime import datetime

class CryptoUtils:
    @staticmethod
    def generate_hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def format_timestamp(timestamp: int) -> str:
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def json_serializable(data) -> str:
        return json.dumps(data, default=str)
    
    @staticmethod
    def parse_price_data(price_data: dict) -> dict:
        if 'price' not in price_data or 'timestamp' not in price_data:
            raise ValueError('Missing price or timestamp in data')
        
        return {
            'hash': CryptoUtils.generate_hash(str(price_data)),
            'formatted_time': CryptoUtils.format_timestamp(price_data['timestamp']),
            'price': price_data['price']
        }
    
    @staticmethod
    def validate_currency_code(currency: str) -> bool:
        accepted_currencies = {'BTC', 'ETH', 'LTC', 'XRP', 'BCH'}
        return currency in accepted_currencies
