from pynput.keyboard import Listener, Key, Controller, KeyCode
import csv


class Recorder:
    buffer = ""

    def __init__(self, word_pairs: dict[str, str]):
        self.keyboard = Controller()
        self.word_pairs = word_pairs

    def on_press(self, key):
        if key == Key.space:
            self.evaluate_word()
            self.buffer = ""
            
        if type(key) is KeyCode:
            self.buffer += key.char if '\\x' not in key.char else ""

    def on_release(self, key):
        pass

    def evaluate_word(self):
        if self.buffer in self.word_pairs:
            self.delete_word()
            self.keyboard.type(self.word_pairs[self.buffer] + " ")

    def delete_word(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        self.keyboard.release(Key.ctrl)


if __name__ == "__main__":
    pairs: dict[str, str] = {}
    with open('replacements.csv', newline='') as f:
        reader = csv.reader(f)
        for item in reader:
            pairs[item[0]] = item[1]

    recorder = Recorder(pairs)

    with Listener(on_press=recorder.on_press, on_release=recorder.on_release) as listener:
        listener.join()
