import os
import vlc
from mutagen.mp3 import MP3


VERBOSE = False  # Set True for debugging


class Sound:

    def __init__(self, name, duration, path):
        self.name = name
        self.dur = duration
        self.path = path

    def getname(self):
        return self.name

    def getpath(self):
        return self.path

    def getdur(self):
        return self.dur

    def rename(self, new_name):
        self.name = new_name

    def remove(self, name):
        pass


default_obj = os.path.abspath("alarm.mp3")
sounds = []


def create_sounds_list():
    path = os.getcwd()+"/Sounds/"
    dir_sounds = os.listdir(path)
    for i, item in enumerate(dir_sounds):
        obj = MP3(path+os.path.basename(item))
        s = Sound(os.path.basename(item), int(obj.info.length), os.path.abspath(os.path.join(path, os.path.basename(item))))
        sounds.append(s)


def print_sounds_list(mylist):
    for i, item in enumerate(mylist):
        print(i, ".", item.getname())


def input_numbers():
    while True:
        num = input()
        if num.isdigit():
            num = int(num)
            return num
        elif num == "":
            return -1
        print("Letters are not accepted")
        print("Pick a number from 0 to ", len(sounds) - 1)


def play_or_exit():
    if not sounds:
        create_sounds_list()
    print_sounds_list(sounds)
    while True:
        print("Choose a number from the list above or click enter to continue \n")
        ans = input_numbers()
        if ans == -1:
            break
        elif 0 <= ans < len(sounds):
            s_player(sounds[ans])
        else:
            print("Pick a number from 0 to ", len(sounds)-1)


def num_or_empty(s):
    if s.isdigit():
        if 0 <= int(s) < len(sounds):
            return int(s)
        else:
            print("Pick a number from the list provided")
            return
    elif s == "":
        return -1
    else:
        print("Only space or numbers are approved")
        return


def change_default(n):
    global default_obj
    default_obj = sounds[n].getpath()


def s_player(item, file=None):
    if file is not None:
        file.stop()
    sf = vlc.MediaPlayer(item.getpath())
    sf.play()
    n_s = input_numbers()
    if n_s != -1:
        s_player(sounds[n_s], sf)
    else:
        sf.stop()


'''def s1_player(item):
    if VERBOSE:
        print("T_end is : ", item.getdur())
    sf = vlc.MediaPlayer(item.getpath())
    sf.play()
    ans1 = Timeisup.time_input("", item.getdur())
    ans1 = num_or_empty(ans1)
    if ans1 is int:
        sf.stop()
        s_player(ans1)
    if ans1 == -1:
        sf.stop()'''
