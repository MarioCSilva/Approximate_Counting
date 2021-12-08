from collections import defaultdict
import re
from utils import open_file
from random import random, seed

class DecreasingProbCounter():
    def __init__(self, fname="datasets/it_book.txt"):
        seed(93430)

        # dictionary with the number of occurrences of each letter
        self.letter_occur = defaultdict(int)

        # reads file in chunks
        # counts the letters and stores the event
        # gets the dictionary with the number of occurrences of each letter
        # using a decreased probability as 1 / 2 ** k
        self.count(fname)

        print(self.letter_occur)


    def count(self, fname):
        file = open_file(fname, 'r')

        k = 0

        # reads chunk by chunk
        while chunk := file.read(1024):
            # removes all non-alphabetical chars
            for letter in re.findall(r'[A-Z]', chunk):
                # counts event with a fixed probability
                if random() <= 1 / 2 ** k:
                    self.letter_occur[letter] += 1
                    k += 1

        file.close

DecreasingProbCounter()