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
        self.counter_value = 0
        decreasing_probability = 1 / self.a ** self.counter_value

        file = open_file(self.fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            # removes all non-alphabetical chars
            for letter in re.findall(r'[A-Z]', chunk):
                # counts event with a decreasing probability
                if random() <= decreasing_probability:
                    self.letter_occur[letter] += 1
                    self.counter_value += 1
                    decreasing_probability = 1 / self.a ** self.counter_value


    def estimated_events(self, num=0):
        if not num:
            num = self.counter_value
        return int(self.a ** num - self.a + 1) / ( self.a - 1 )

