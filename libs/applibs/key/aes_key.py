from Crypto.Cipher import AES
import base64

def generate_key_and_nonce(key):
    key = key.encode()
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    
    nonce_bytes = base64.b64encode(nonce)
    nonce_string = nonce_bytes.decode()
    
    return key, nonce_string

def encrypt(data, key=None, nonce=None):
    cipher = AES.new(key.encode(), AES.MODE_EAX, nonce=base64.b64decode(nonce.encode()))
    
    data = data.encode()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    encrypted_bytes = base64.b64encode(ciphertext)
    encrypted_string = encrypted_bytes.decode()
    
    return encrypted_string

def decrypt(data, key=None, nonce=None):
    cipher = AES.new(key.encode(), AES.MODE_EAX, nonce=base64.b64decode(nonce.encode()))
    
    encrypted_bytes = data.encode()
    ciphertext = base64.b64decode(encrypted_bytes)
    decrypted_text = cipher.decrypt(ciphertext)
    
    return decrypted_text.decode('utf-8')


'''
---base64 bytes to string string to bytes, example---

import base64

base64_bytes = base64.b64encode(b'\x9cJt\x11\xecN\xae\xa5Z"1K\x03\x12\xe6\xf0')
base64_string = base64_bytes.decode()

base64_bytes = 'nEp0EexOrqVaIjFLAxLm8A=='.encode()
sample_string_bytes = base64.b64decode(base64_bytes)
'''