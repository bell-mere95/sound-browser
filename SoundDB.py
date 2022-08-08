import os
import vlc
import sqlite3
from sqlite3 import Error
from mutagen.mp3 import MP3
from SoundBrowser import input_numbers


sql_check = """SELECT * FROM sounds"""
sql_create_sounds_table = """ CREATE TABLE IF NOT EXISTS sounds (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        duration NOT NULL,
                                        path text NOT NULL
                                    ); """
VERBOSE = False  # Set True for debugging


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("successful connection")
        return conn
    except Error:
        print("fail at creation of database")
    return conn


def create_table(conn, sql_com):
    try:
        c = conn.cursor()
        c.execute(sql_com)
        rows = c.execute(sql_check).fetchall()
        if not rows:
            initial_fill_database(conn)
    except Error:
        print("fail to create table")


def initial_fill_database(conn):
    path = os.getcwd() + "/Sounds/"
    dir_sounds = os.listdir(path)
    sql_com = ''' INSERT INTO sounds(name,duration,path) VALUES(?,?,?) ;'''
    for i, item in enumerate(dir_sounds):
        obj = MP3(path + os.path.basename(item))
        sound = (os.path.basename(item), int(obj.info.length), os.path.abspath(os.path.join(path, os.path.basename(item))))
        cur = conn.cursor()
        cur.execute(sql_com, sound)
        conn.commit()


def print_sounds_list(conn):
    cursor = conn.cursor()
    sql_com = """SELECT * from sounds"""
    cursor.execute(sql_com)
    sounds = cursor.fetchall()
    conn.commit()
    for sound in sounds:
        print(sound[0], ". ", sound[1])


def insert_row(conn, row):
    sql_row = """INSERT INTO sounds(name,duration,path) VALUES (?,?,?);"""
    c = conn.cursor()
    c.execute(sql_row, row)
    c.commit()


def search_in_db(conn, n):
    c = conn.cursor()
    sql_row = """SELECT * FROM sounds WHERE id=?"""
    c.execute(sql_row, (n,))
    sound = c.fetchone()
    conn.commit()
    return sound


def s_player_db(conn, row, n, file=None):
    if file is not None:
        file.stop()
    # print(row[1], " Now playing")
    sf = vlc.MediaPlayer(row[3])
    sf.play()
    n_s = input_numbers()
    if n_s == -1:
        sf.stop()
    elif 1 <= n_s <= n:
        s_player_db(conn, search_in_db(conn, n_s), n, sf)
    else:
        print("You can pick a number from 1 to ", n)


def play_or_exit_db():
    conn = create_connection("sounds.db")
    create_table(conn, sql_create_sounds_table)
    print_sounds_list(conn)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM Sounds")
    n_sounds = c.fetchone()[0]
    conn.commit()
    # print(n_sounds)
    while True:
        print("Choose a number from the list above or click enter to continue \n")
        ans = input_numbers()
        if ans == -1:
            break
        elif 0 < ans <= n_sounds:
            s_player_db(conn, search_in_db(conn, ans), n_sounds)
        else:
            print("Pick a number from 1 to ", n_sounds)


def set_default():
    pass


def get_default():
    pass


def delete_from_db():
    pass


def delete_database():
    pass
