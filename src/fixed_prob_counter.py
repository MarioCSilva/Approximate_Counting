from collections import defaultdict
import re
from utils import open_file
from random import random, seed


class FixedProbCounter():
    def __init__(self, fname="../datasets/it_book.txt"):
        seed(93430)

        self.fname = fname

        self.fixed_probability = 1 / 8

    
    def __str__(self):
        return "Fixed Probability Counter with 1 / 8"


    '''Reads file in chunks
       counts the letters and stores the event
       gets the dictionary with the number of occurrences of each letter
       using a fixed probability of 1 / 8
    '''
    def count(self):
        self.letter_occur = defaultdict(int)
        self.counter_value = 0

        file = open_file(self.fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            # removes all non-alphabetical chars
            for letter in re.findall(r'[A-Z]', chunk):
                # counts event with a fixed probability
                if random() <= self.fixed_probability:
                    self.letter_occur[letter] += 1
                    self.counter_value += 1

        file.close


    def estimated_events(self, num=0):
        if not num:
            num = self.counter_value
        return int(num * (1 / self.fixed_probability))
    

