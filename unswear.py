from pynput.keyboard import Listener, Key, Controller, KeyCode
import csv

from pystray import Menu, MenuItem, Icon
from webbrowser import open as open_link
from PIL import Image

class Recorder:
    buffer = ""

    def __init__(self, word_pairs: dict[str, str], icon_tray):
        self.keyboard = Controller()
        self.word_pairs = word_pairs
        self.icon_tray = icon_tray

    def on_press(self, key):
        if key == Key.space:
            self.evaluate_word()
            self.buffer = ""

        if key == Key.backspace:
            self.handle_backspace()

        if type(key) is KeyCode and key.char is not None:
            self.buffer += key.char

    def handle_backspace(self):
        self.buffer = self.buffer[:-1]

    def on_release(self, key):
        pass

    def evaluate_word(self):
        if self.buffer in self.word_pairs:
            self.delete_word(len(self.buffer))
            self.keyboard.type(self.word_pairs[self.buffer] + " ")

    def delete_word(self, length):
        for i in range(length + 1):
            self.keyboard.press(Key.backspace)
            self.keyboard.release(Key.backspace)

def on_quit(icon_tray, recorder):
    icon_tray.stop()
    recorder.listener.stop()

def open_git():
    url = 'https://github.com/mhavelka77/unSwear'
    open_link(url)

if __name__ == "__main__":
    pairs: dict[str, str] = {}
    with open('replacements.csv', newline='') as f:
        reader = csv.reader(f)
        for item in reader:
            pairs[item[0]] = item[1]

    tray_icon = Icon('name', Image.open('snail.ico'))
    tray_icon.title = 'Right click for options'
    recorder = Recorder(pairs, tray_icon)
    tray_icon.menu = Menu(MenuItem('Open Git', open_git),
        MenuItem('Quit', lambda: on_quit(tray_icon, recorder))
    )

    recorder.listener = Listener(on_press=recorder.on_press, on_release=recorder.on_release) # type: ignore
    recorder.listener.start() # type: ignore
    tray_icon.run()