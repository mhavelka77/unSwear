import csv
from typing import Dict

from pynput.keyboard import Controller, Key, KeyCode, Listener


class Recorder:
    """
    A class to record and evaluate typed words.

    Attributes:
        word_pairs (Dict[str, str]): A dictionary of words to be replaced and their corresponding replacement.
        buffer (str): A buffer to store the current word being typed.
        keyboard (Controller): A controller to handle keyboard input.
    """

    def __init__(self, pairs: Dict[str, str]):
        """
        Initializes the Recorder with the given word pairs.

        :param pairs: A dictionary of words to be replaced and their corresponding replacement.
        """
        self.keyboard = Controller()
        self.word_pairs = pairs
        self.buffer = ""

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


if __name__ == "__main__":
    word_pairs: Dict[str, str] = {}
    with open('replacements.csv', newline='') as f:
        reader = csv.reader(f)
        for item in reader:
            word_pairs[item[0]] = item[1]

    recorder = Recorder(word_pairs)

    with Listener(on_press=recorder.on_press, on_release=recorder.on_release) as listener:
        listener.join()
