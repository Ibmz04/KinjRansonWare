import os
from Crypto.Cipher import AES
from Crypto.Util import Padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



class decryption_setup:
    def __init__(self, key):
        self.key = key
        self.decryption_key = self.generate_key()

    def generate_key(self):
        salt = b'salt_'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = kdf.derive(self.key.encode())
        return key

    def AES_CBC_256(self, path):
        with open(path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        iv = encrypted_data[-16:]
        cipher = AES.new(self.decryption_key, AES.MODE_CBC, iv)
        normal_data = cipher.decrypt(encrypted_data[18: -16:])
        unpadding_data = Padding.unpad(normal_data, 16)
        with open(path[:-5], 'wb') as normal_file:
            normal_file.write(unpadding_data)
        os.remove(path)

