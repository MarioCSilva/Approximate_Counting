from collections import defaultdict
import re
from utils import open_file
from random import random, seed


class DecreasingProbCounter():
    def __init__(self, fname="../datasets/it_book.txt"):
        seed(93430)

        self.fname = fname

        self.a = 2


    def __str__(self) -> str:
        return "Decreasing Probability Counter with 1 / 2^k"


    '''Reads file in chunks
       Counts the letters and stores the event
       Gets the dictionary with the number of occurrences of each letter
       Using a decreased probability as 1 / 2 ** k
    '''
    def count(self):
        self.letter_occur = defaultdict(int)
        letter_probabilities = defaultdict(lambda: 1)

        file = open_file(self.fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            # removes all non-alphabetical chars
            for letter in chunk:
                if letter.isalpha():
                    letter = letter.upper()
                    # counts event with a decreasing probability
                    if random() <= letter_probabilities[letter]:
                        self.letter_occur[letter] += 1
                        letter_probabilities[letter] = 1 / self.a ** self.letter_occur[letter]

        file.close()


    def estimate_events(self):
        self.estimated_letter_occur = {}
        for letter, occur in self.letter_occur.items():
            self.estimated_letter_occur[letter] = int(self.a ** occur - 1)

