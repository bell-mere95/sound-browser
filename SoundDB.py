import os
import vlc
import sqlite3
from sqlite3 import Error
from mutagen.mp3 import MP3
from SoundBrowser import input_numbers

VERBOSE = False  # Set True for debugging


def sql_create_table(t_name):
    sql = "CREATE TABLE IF NOT EXISTS %s (id integer PRIMARY KEY,name text NOT NULL, duration NOT NULL, path text NOT NULL); " % t_name
    return sql


def sql_select(t_name):
    sql = "SELECT * FROM %s" % t_name
    return sql


def sql_delete(t_name, column):
    sql = "DELETE FROM %s WHERE %s=?" % (t_name, column)
    return sql


def sql_insert(t_name):
    sql = "INSERT INTO %s (name, duration, path) VALUES (?,?,?)" % t_name
    return sql


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error:
        print("fail at creation of database")
    return conn


def create_table(conn, name):
    try:
        c = conn.cursor()
        c.execute(sql_create_table(name))
        rows = c.execute(sql_select("sounds")).fetchall()
        if not rows:
            initial_fill_database(conn)
    except Error:
        print("fail to create table")


def initial_fill_database(conn):
    path = os.getcwd() + "/Sounds/"
    dir_sounds = os.listdir(path)
    for i, item in enumerate(dir_sounds):
        obj = MP3(path + os.path.basename(item))
        sound = (os.path.basename(item), int(obj.info.length), os.path.abspath(os.path.join(path, os.path.basename(item))))
        try:
            cur = conn.cursor()
            cur.execute(sql_insert("sounds"), sound)
            conn.commit()
        except Error:
            print("Fail to fill sounds table")


def print_sounds_list(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_select("sounds"))
        sounds = cursor.fetchall()
        conn.commit()
        for sound in sounds:
            print(sound[0], ". ", sound[1])
    except Error:
        print("Fail to print sounds list")


def insert_row(conn, row):
    try:
        c = conn.cursor()
        c.execute(sql_insert("sounds"), row)
        c.commit()
    except Error:
        print("Fail to insert row at sounds table")


def search_in_db(conn, n):
    try:
        c = conn.cursor()
        sql_row = """SELECT * FROM sounds WHERE id=?"""
        c.execute(sql_row, (n,))
        sound = c.fetchone()
        conn.commit()
        return sound[1:]
    except Error:
        print("Fail to find sound")
        return


def s_player_db(conn, row, n, file=None):
    if file is not None:
        file.stop()
    sf = vlc.MediaPlayer(row[2])
    sf.play()
    n_s = input_numbers()
    if n_s == -1:
        sf.stop()
    elif n_s == 0:
        sf.stop()
        set_default(conn, row)
        print("Favourite has changed successfully! ")
    elif 1 <= n_s <= n:
        s_player_db(conn, search_in_db(conn, n_s), n, sf)
    else:
        print("You can pick a number from 1 to ", n)


def intro():
    conn = create_connection("sounds.db")
    create_default(conn)
    print("Welcome!\n")
    while True:
        choose = input("%s is selected. Hit any key to change it or Enter for exit" % get_default(conn))
        if choose == "":
            print("Goodbye!")
            break
        else:
            play_or_exit_db(conn)


def play_or_exit_db(conn):
    create_table(conn, "sounds")
    print_sounds_list(conn)
    try:
        c = conn.cursor()
        c.execute(sql_select("sounds"))
        n_sounds = len(c.fetchall())
        conn.commit()
        print("Choose a number from the list above and 0 to change it or click enter to continue \n")
        ans = input_numbers()
        if 0 < ans <= n_sounds:
            s_player_db(conn, search_in_db(conn, ans), n_sounds)
        else:
            print("Pick a number from 1 to ", n_sounds)
    except Error:
        print("Session failed")


def create_default(conn):
    path = os.getcwd() + "/Sounds/"
    obj = MP3(path + "Alarm.mp3")
    try:
        c = conn.cursor()
        c.execute(sql_create_table("favourite"))
        c.execute(sql_insert("favourite"),  ("Alarm.mp3", int(obj.info.length), os.path.abspath(os.path.join(path, "Alarm.mp3"))))
        conn.commit()
    except Error:
        print("Fail to create favourite table")


def set_default(conn, row=None):
    if row is None:
        create_default(conn)
    else:
        try:
            c = conn.cursor()
            c.execute(sql_select("favourite"))
            pre_fav = c.fetchone()[1]
            delete_from_table(conn, "favourite", "name", pre_fav)
            c.execute(sql_insert("favourite"), row)
            conn.commit()
        except Error:
            print("Fail to select a new sound as favourite")


def get_default(conn):
    try:
        c = conn.cursor()
        c.execute(sql_select("favourite"))
        return c.fetchone()[1]
    except Error:
        print("Fail to print your favourite")
        return


def delete_from_table(conn, table, column, value):
    try:
        c = conn.cursor()
        c.execute(sql_delete(table, column), (value,))
        conn.commit()
    except Error:
        print("Fail to delete row")
