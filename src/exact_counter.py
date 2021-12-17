from collections import defaultdict
import re
from utils import open_file


class ExactCounter():
    def __init__(self, fname="../datasets/it_book.txt"):
        self.fname = fname

    
    def __str__(self):
        return "Exact Counter"


    '''Reads file in chunks
       counts the letters and stores the event
       gets the dictionary with the exact number of occurrences of each letter
    '''
    def count(self):
        self.letter_occur = defaultdict(int)
        self.counter_value = 0

        file = open_file(self.fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            # removes all non-alphabetical chars
            for letter in re.findall(r'[A-Z]', chunk):
                self.letter_occur[letter] += 1
                self.counter_value += 1
        
        file.close


    def top_k_letters(self, k=10):
        return {letter: occur for letter, occur in \
            sorted(self.letter_occur.items(), key=lambda x: x[1], reverse=True)[:k]}