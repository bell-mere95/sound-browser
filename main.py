import SoundBrowser
import SoundDB

db = True  # Set True to use database or False to use class instances

if __name__ == '__main__':
        if db:
        SoundDB.play_or_exit_db()
    else:
        SoundBrowser.play_or_exit()
