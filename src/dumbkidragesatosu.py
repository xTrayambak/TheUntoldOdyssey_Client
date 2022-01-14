import random

class Combination:
    def __init__(self, words: list):
        self.words = list(words)

    def shuffle(self):
        random.shuffle(self.words)

        return self.words

    def __call__(self):
        return self.words

def laz():
    sentence = "Dumb kid rages at Osu"
    words = sentence.split(" ")

    combinations = []

    used = []

    for x in range(len(words)*len(words)):
        combination = Combination(words)
        combination.shuffle()

        while combination() in used:
            combination.shuffle()
            print(f"Trying {combination()}")

        used.append(combination())
        combinations.append(combination())
        

    return combinations

if __name__ == "__main__":
    print("Testing")
    for combination in laz():
        string = ""
        for letter in combination:
            string += letter + " "
        
        print(string)