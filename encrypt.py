import base64, random, string, os
from Crypto.Cipher import AES

def aes_encrypt(content, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(content.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def write_encrypted_file(input_file):
    with open(input_file, 'r') as f:
        content = f.read()
    aes_key = os.urandom(16)
    with open('enc.py', 'w') as f:
        f.write(f"encrypted = '{aes_encrypt(content, aes_key)}'\naes_key = '{base64.b64encode(aes_key).decode()}'")
        f.write('''\n
from Crypto.Cipher import AES
import base64

def decrypt(encrypted, key):
    encrypted = base64.b64decode(encrypted)
    return AES.new(base64.b64decode(key), AES.MODE_EAX, nonce=encrypted[:16]).decrypt_and_verify(encrypted[32:], encrypted[16:32]).decode()

exec(decrypt(encrypted, aes_key))''')
write_encrypted_file(input("File name:"))