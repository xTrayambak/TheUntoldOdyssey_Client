import random
import time

class Combination:
    def __init__(self, words: list):
        self.words = list(words)

    def shuffle(self):
        random.shuffle(self.words)

        return self.words

    def __call__(self):
        return self.words

def laz():
    sentence = input("gimme sentence >>> ")
    words = sentence.split(" ")
    spaces = len(words)-1

    combinations = []

    print(words)

    used = []

    for x in range(len(words)*spaces):
        combination = Combination(words)
        combination.shuffle()

        while combination() in used:
            combination.shuffle()
            #print(f"Trying {combination()}")

        used.append(combination())
        combinations.append(combination())

    return combinations

if __name__ == "__main__":
    for combination in laz():
        string = ""
        for char in combination:
            string += char + " "
        print(string)