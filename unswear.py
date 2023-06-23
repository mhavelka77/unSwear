import csv
from typing import Dict

from pynput.keyboard import Controller, Key, KeyCode, Listener

from pystray import Menu, MenuItem, Icon
from webbrowser import open as open_link
from PIL import Image

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    """
    A file change event handler that monitors modifications to the 'replacements.csv' file.

    Attributes:
        recorder (Recorder): An instance of the Recorder class.
    """

    def __init__(self, recorder):
        """
        Initializes the FileChangeHandler with the given Recorder instance.

        :param recorder (Recorder): An instance of the Recorder class.
        """
        self.recorder = recorder

    def on_modified(self, event):
        """
        Callback method triggered when a file modification event occurs.

        If the modified file is 'replacements.csv', it calls the
        update_word_pairs() method of the associated Recorder instance.

        :param event (FileSystemEvent): The file system event object representing the modification event.
        """
        if event.src_path.endswith('replacements.csv'):
            try:
                self.recorder.update_word_pairs()
            except IndexError:
                pass


class Recorder:
    """
    A class to record and evaluate typed words.

    Attributes:
        word_pairs (Dict[str, str]): A dictionary of words to be replaced and their corresponding replacement.
        buffer (str): A buffer to store the current word being typed.
        keyboard (Controller): A controller to handle keyboard input.
    """

    def __init__(self, pairs: Dict[str, str], icon_tray):
        """
        Initializes the Recorder with the given word pairs.

        :param pairs: A dictionary of words to be replaced and their corresponding replacement.
        """
        self.keyboard = Controller()
        self.word_pairs = pairs
        self.buffer = ""
        self.icon_tray = icon_tray

    def on_press(self, key):
        """
        Handles key press events.

        :param key: The key that was pressed.
        """
        if key == Key.space:
            self.evaluate_word()
            self.buffer = ""

        if key == Key.backspace:
            self.handle_backspace()

        if type(key) is KeyCode and key.char is not None:
            self.buffer += key.char

    def handle_backspace(self):
        """
        Handles backspace events by removing the last character from the buffer.
        """
        self.buffer = self.buffer[:-1]

    def on_release(self, key):
        """
        Handles key release events.

        :param key: The key that was released.
        """
        pass

    def evaluate_word(self):
        """
        Evaluates the current word in the buffer and replaces it if necessary.
        """
        if self.buffer in self.word_pairs:
            self.delete_word(len(self.buffer))
            self.keyboard.type(f"{self.word_pairs[self.buffer]} ")

    def delete_word(self, length):
        """
        Deletes the current word by sending backspace events.

        :param length: The length of the word to be deleted.
        """
        for _ in range(length + 1):
            self.keyboard.press(Key.backspace)
            self.keyboard.release(Key.backspace)

    def update_word_pairs(self):
        """
        Updates the word pairs in the Recorder object based on the contents of the 'replacements.csv' file.
        """
        word_pairs: Dict[str, str] = {}
        with open('replacements.csv', newline='') as f:
            reader = csv.reader(f)
            for item in reader:
                word_pairs[item[0]] = item[1]
        self.word_pairs = word_pairs
        print("Updates")


def on_quit(icon_tray, recorder, observer):
    observer.stop()
    icon_tray.stop()
    recorder.listener.stop()


def open_git():
    url = 'https://github.com/mhavelka77/unSwear'
    open_link(url)


if __name__ == "__main__":
    word_pairs: Dict[str, str] = {}
    with open('replacements.csv', newline='') as f:
        reader = csv.reader(f)
        for item in reader:
            word_pairs[item[0]] = item[1]

    tray_icon = Icon('name', Image.open('snail.ico'))
    tray_icon.title = 'Right click for options'
    recorder = Recorder(word_pairs, tray_icon)
    tray_icon.menu = Menu(MenuItem('Open Git', open_git),
        MenuItem('Quit', lambda: on_quit(tray_icon, recorder))
    )

    recorder.listener = Listener(on_press=recorder.on_press, on_release=recorder.on_release)    # type: ignore
    recorder.listener.start()   # type: ignore

    event_handler = FileChangeHandler(recorder)
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()

    tray_icon.run()
