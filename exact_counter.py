from collections import defaultdict
import re
from utils import open_file

class ExactCounter():
    def __init__(self, fname="datasets/it_book.txt"):
        # dictionary with the number of occurrences of each letter
        self.letter_occur = defaultdict(int)

        # reads file in chunks
        # counts the letters and stores the event
        # gets the dictionary with the exact number of occurrences of each letter
        self.count(fname)

        print(self.letter_occur)


    def count(self, fname):
        file = open_file(fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            # removes all non-alphabetical chars
            for letter in re.findall(r'[A-Z]', chunk):
                self.letter_occur[letter] += 1

        file.close

ExactCounter()