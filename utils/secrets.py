import random
import base64
import json


secret_key = "A"

def generate_random_slice(length: int) -> str:
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(characters) for _ in range(length))

def encode(str: str, key: str = secret_key, slice_length: int = 8) -> str:
    text_bytes = str.encode('utf-8')
    key_bytes = key.encode('utf-8')
    
    encoded_bytes = [text_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(text_bytes))]
    
    encoded_string = base64.b64encode(bytes(encoded_bytes)).decode('utf-8')
    
    random_start = generate_random_slice(slice_length)
    random_end = generate_random_slice(slice_length)
    
    return random_start + encoded_string + random_end

def decode(encoded_str: str, key: str = secret_key, slice_length: int = 8) -> str:
    sliced_str = encoded_str[slice_length:-slice_length]
    
    decoded_bytes = base64.b64decode(sliced_str)
    key_bytes = key.encode('utf-8')
    
    decoded_text_bytes = [decoded_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(decoded_bytes))]
    
    return bytes(decoded_text_bytes).decode('utf-8')


def jsonify(data: str):
    try:
        return json.loads(data)
    except:
        return {}