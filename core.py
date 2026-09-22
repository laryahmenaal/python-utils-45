import hashlib
import hmac

def validate_payload(data):
    required = {'nonce', 'signature', 'payload'}
    if not all(k in data for k in required):
        return False
    if not isinstance(data['nonce'], int) or data['nonce'] < 0:
        return False
    return True

def process_stream(data_stream, secret):
    processed = []
    for entry in data_stream:
        try:
            if not validate_payload(entry):
                print(f"dropping malformed packet: {entry.get('nonce')}")
                continue
            
            computed = hmac.new(secret.encode(), str(entry['payload']).encode(), hashlib.sha256).hexdigest()
            if hmac.compare_digest(computed, entry['signature']):
                processed.append(entry['payload'])
        except Exception as e:
            print(f"encryption-level anomaly caught: {e}")
    return processed

if __name__ == '__main__':
    # usage example
    sample = [{'nonce': 1, 'signature': 'abc', 'payload': 'test'}]
    results = process_stream(sample, 'supersecret')
    print(f"valid entries: {len(results)}")