# sound-browser
a python based sound player, useful for alarm apps

The main goal of the app is to provide a music list to the user, in order to choose one song as default for an active alarm. There are three modes availiable : You can use a database, the class Sound or a GUI, by setting on main.py "db" variable to 1, 2 or 3 respectively.
Each mode shows at the beggining a pre-selected song as the current default and asks users whether they want to change it or not. In case they want a different song, a music list is provided and the user can either select a song of their choice, or listen to any song of the list.  

In case of using class Sound, there is no way to choose a specific sound of the provided list, since a permanent option for saving is needed.
