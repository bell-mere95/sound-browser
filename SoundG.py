import sqlite3
from sqlite3 import Error
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
import SoundDB
import vlc

conn = sqlite3.connect('sounds.db')
cur = conn.cursor()


def clear_frame(f):
    for widget in f.winfo_children():
        if type(widget) == tk.Button:
            widget.destroy()


def search_in_db(n):
    try:
        sql_row = """SELECT * FROM sounds WHERE id=?"""
        cur.execute(sql_row, (n,))
        sound = cur.fetchone()
        conn.commit()
        return sound[1:]
    except Error:
        print("Fail to find sound")
        return


def s_player(row, file=None):
    if file is not None:
        file.stop()
    sf = vlc.MediaPlayer(row[2])
    sf.play()


class Welcome:
    def __init__(self, master):
        self.master = master
        self.master.geometry('380x120')
        self.master.title("Welcome to Sound Browser")
        f = Frame(self.master, height=115, width=350)
        f.pack(side="top", pady=15)
        lab = Label(f, text="Welcome!")
        lab.pack(side="top")
        lab.after(3000, f.destroy)


class MyGui:
    def __init__(self, master):
        self.master = master
        self.master.geometry('380x120')
        self.frame = Frame(self.master, height=115, width=350)
        self.frame.pack()
        self.master.title('Sound Browser - Default Song')
        self.label = Label(self.frame, text="%s is selected. Would you like to change it?" % SoundDB.get_default(conn))
        self.label.pack(side="top", pady=15)
        self.button1 = Button(self.frame, text="Exit", command=self.bye)
        self.button1.pack(side="left", padx=25)
        self.button2 = Button(self.frame, text="Change", command=self.change)
        self.button2.pack(side="right", padx=25)

    def bye(self):
        self.label.config(text="Goodbye!")
        clear_frame(self.frame)
        self.master.after(2000, self.master.destroy)

    def change(self):
        self.frame.destroy()
        PlayOrExit(self.master)


class PlayOrExit:
    def __init__(self, master):
        self.master = master
        self.master.geometry('320x650')
        self.master.title('Sound List')
        self.frameB = Frame(self.master)
        self.frameB.pack(fill="x", side="top")
        self.frame = Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        self.button1 = Button(self.frameB, text="Play", fg="blue", command=self.play)
        self.button2 = Button(self.frameB, text="Return to home", fg="red", command=self.home)
        self.button3 = Button(self.frameB, text="Submit", fg="Green", command=self.soundChoice)
        self.button1.pack(padx=10, side="left")
        self.button2.pack(padx=10, side="right")
        self.button3.pack(padx=10, anchor="n")
        self.mylist = Listbox(self.frame)
        SoundDB.create_table(conn, "sounds")
        self.print_sound_list()

    def play(self):
        ls = self.mylist.curselection()
        for item in ls:
            song = search_in_db(item+1)
            s_player(song)

    def home(self):
        self.frame.destroy()
        self.frameB.destroy()
        MyGui(self.master)

    def print_sound_list(self):
        try:
            cursor = conn.cursor()
            cursor.execute(SoundDB.sql_select("sounds"))
            sounds = cursor.fetchall()
            conn.commit()
            for sound in sounds:
                self.mylist.insert(sound[0], sound[1])
            self.mylist.pack(padx=10, pady=10, expand=YES, fill="both")
            self.mylist.bind("<<ListboxSelect>>", self.soundChoice())
        except Error:
            print("Fail to print sounds list")

    def soundChoice(self):
        ls = self.mylist.curselection()
        for item in ls:
            SoundDB.set_default(conn, search_in_db(item+1))


class App:
    def __init__(self, master):
        self.master = master
        Welcome(master)
        self.master.after(3000, MyGui, master)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()
