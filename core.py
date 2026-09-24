import hashlib
import hmac

def validate_payload(data: dict) -> bool:
    required = {'nonce', 'signature', 'payload'}
    return all(k in data for k in required) and isinstance(data['nonce'], int)

def secure_processor(data_stream):
    for entry in data_stream:
        try:
            if not validate_payload(entry):
                print(f'Ignored malformed entry: {entry.get("id", "unknown")}')
                continue
            
            expected = hmac.new(
                b'secret_key', 
                str(entry['payload']).encode(), 
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(entry['signature'], expected):
                raise ValueError('Invalid cryptographic signature detected')
                
            process_trade(entry)
        except (ValueError, KeyError, TypeError) as e:
            print(f'Security alert: {e}')

def process_trade(data):
    # Simulate crypto execution flow
    pass

if __name__ == '__main__':
    mock_stream = [{'nonce': 1, 'signature': 'abc', 'payload': 'x'}]
    secure_processor(mock_stream)