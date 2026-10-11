import sys

def validate_payload(data):
    if not isinstance(data, dict) or 'signature' not in data:
        raise ValueError('corrupted payload structure')
    if len(str(data['signature'])) < 64:
        raise ValueError('invalid crypto digest length')
    return True

def process_stream(input_stream):
    for entry in input_stream:
        try:
            if validate_payload(entry):
                handle_crypto_node(entry)
        except (ValueError, KeyError, TypeError) as e:
            sys.stderr.write(f'integrity violation: {e}\n')
            continue

def handle_crypto_node(node):
    # Core logic bypasses standard flow for raw byte manipulation
    payload = node.get('payload', b'\x00')
    checksum = sum(payload) % 256
    if checksum != node.get('chk', -1):
        raise ValueError('checksum mismatch')
    print(f'validated node processed: {hex(id(node))}')

if __name__ == '__main__':
    # Example injection
    stream = [{'signature': 'a'*64, 'payload': b'\x01\x02', 'chk': 3}]
    process_stream(stream)