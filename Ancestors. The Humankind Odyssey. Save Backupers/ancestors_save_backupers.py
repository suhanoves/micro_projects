import os
import shutil
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

"""
This script allows you to make backups of the game saves
Ancestors: The Humankind Odyssey.
This game is automatically saved in only one file, without any backups.
After starting the game, you need to run this script,
it automatically tracks changes to the save file and makes a backup during autosave.
This way you can return at any point in the game.

Don't forget to change USER name.

#pip install watchdog
"""

USER = 'suhanoves'
SOURCE_PATH = f'C:/Users/{USER}/AppData/Local/Ancestors/Saved/SaveGames/'
BACKUP_PATH = f'C:/Users/{USER}/AppData/Local/Ancestors/Saved/SaveBackups/'


def backup(source_path, backup_path, file):
    time.sleep(15)
    today = datetime.today()
    today_string = f'{today.strftime("%d.%m.%y")} {today.strftime("%H-%M-%S")}'

    source = rf"{source_path}{file}"
    destination = f'{backup_path}{today_string} {file}'

    operation_copy = shutil.copy(source, destination)
    print(f"{datetime.today().strftime('%H:%M:%S')} File copied:", operation_copy)


def create_backup(file):
    files = os.listdir(SOURCE_PATH)
    for item in files:
        if item == file:
            backup(SOURCE_PATH, BACKUP_PATH, item)

    # print(f'\nBackup folder:{os.listdir(BACKUP_PATH)}')


def on_created(event):
    print(f"\n{datetime.today().strftime('%H:%M:%S')} created file {event.src_path}")
    file = event.src_path.split("/")[-1]
    create_backup(file)


def on_deleted(event):
    print(f"\ndeleted file {event.src_path}!")


def on_modified(event):
    print(f"\n{datetime.today().strftime('%H:%M:%S')} modified file {event.src_path}")
    file = event.src_path.split("/")[-1]
    create_backup(file)


def on_moved(event):
    print(f"moved file {event.src_path} to {event.dest_path}")


# The event handler is the object that will be notified
# when something happen # on the filesystem you are monitoring.
if __name__ == "__main__":
    patterns = "*Savegame*"
    ignore_patterns = ""
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns,
                                                   ignore_patterns,
                                                   ignore_directories,
                                                   case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_modified = on_modified
    # my_event_handler.on_deleted = on_deleted
    # my_event_handler.on_moved = on_moved

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, SOURCE_PATH, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('exit')
        my_observer.stop()
        my_observer.join()
