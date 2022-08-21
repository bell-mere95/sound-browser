import SoundBrowser
import SoundDB

db = 1  # Set 1 to use database, 2 to use class instances or 3 to use GUI

if __name__ == '__main__':
    if db == 1:
        SoundDB.intro()
    elif db == 2:
        SoundBrowser.play_or_exit()
    elif db == 3:
        SoundG.main()
    else:
        print("You need set db variable as 1, 2 or 3. See the comment above")
