from pynput.keyboard import Listener, Key, Controller
import csv

class Recorder:
    buffer = ""

    def __init__(self, wordPairs):
        self.keyboard = Controller()
        self.wordPairs = wordPairs

    def on_press(self, key):
        if key == Key.space: 
            self.evaluateWord()        
            self.buffer = ""
        else:
            try: 
                self.buffer += key.char
            except:
                pass

    def on_release(self, key):
        pass 

    def evaluateWord(self):
        for i in range(len(self.wordPairs)):
            if self.wordPairs[i][0] in self.buffer:
                for n in range(len(self.buffer) + 1):
                    self.keyboard.press(Key.backspace)
                    self.keyboard.release(Key.backspace)
                self.keyboard.type(self.wordPairs[i][1] + " ")


if __name__ == "__main__":

    with open('replacements.csv', newline='') as f:
        reader = csv.reader(f)
        wordPairs = list(reader)

    recorder = Recorder(wordPairs)

    with Listener(on_press=recorder.on_press, on_release=recorder.on_release) as listener:
        listener.join()
