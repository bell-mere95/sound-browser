import SoundBrowser
import SoundDB

db = True  # Set True to use database or False to use class instances
sql_create_sounds_table = """ CREATE TABLE IF NOT EXISTS sounds (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        duration NOT NULL,
                                        path text NOT NULL
                                    ); """
sql_check = """SELECT * FROM sounds"""

if __name__ == '__main__':
        if db:
        SoundDB.play_or_exit_db()
    else:
        SoundBrowser.play_or_exit()
