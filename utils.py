import hashlib
import base64
import secrets

def generate_key(length=32):
    return secrets.token_hex(length)

def double_hash(data):
    first = hashlib.sha256(data.encode()).digest()
    reversed_first = first[::-1]
    return hashlib.sha256(reversed_first).hexdigest()

def xor_encrypt(plaintext, key):
    if not key:
        key = "defaultkey"
    key_bytes = key.encode()
    key_len = len(key_bytes)
    encrypted = bytearray()
    for i, char in enumerate(plaintext.encode()):
        encrypted.append(char ^ key_bytes[i % key_len])
    return base64.b64encode(encrypted).decode()

def xor_decrypt(ciphertext, key):
    if not key:
        key = "defaultkey"
    key_bytes = key.encode()
    key_len = len(key_bytes)
    encrypted = base64.b64decode(ciphertext)
    decrypted = bytearray()
    for i, byte in enumerate(encrypted):
        decrypted.append(byte ^ key_bytes[i % key_len])
    return decrypted.decode()

def hash_with_salt(data, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)
    combined = data.encode() + salt
    return hashlib.sha512(combined).hexdigest()

def validate_key(key):
    if len(key) < 8 or len(key) % 2 != 0:
        return False
    return len(set(key)) >= 3