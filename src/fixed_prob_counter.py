from collections import defaultdict
import re
from utils import open_file
from random import random, seed


class FixedProbCounter():
    def __init__(self, fname="datasets/it_book.txt"):
        seed(93430)

        # dictionary with the number of occurrences of each letter
        self.letter_occur = defaultdict(int)
        self.fixed_probability = 1 / 8

        # reads file in chunks
        # counts the letters and stores the event
        # gets the dictionary with the number of occurrences of each letter
        # using a fixed probability of 1 / 8
        self.count(fname)


    def count(self, fname):
        file = open_file(fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            # removes all non-alphabetical chars
            for letter in re.findall(r'[A-Z]', chunk):
                # counts event with a fixed probability
                if random() <= self.fixed_probability:
                    self.letter_occur[letter] += 1

        file.close

FixedProbCounter()