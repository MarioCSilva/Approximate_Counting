from decr_prob_counter import DecreasingProbCounter
from exact_counter import ExactCounter
from fixed_prob_counter import FixedProbCounter
import time


class Test():
    def __init__(self, fname="datasets/it_book.txt", repetitions = 1000, k=10):
        self.fname = fname
        self.repetitions = repetitions
        self.k = k

        self.run_test()


    def run_test(self):
        exact_counter, fixed_prob_counter, decr_prob_counter =\
            ExactCounter(self.fname), FixedProbCounter(self.fname), DecreasingProbCounter(self.fname)

        self.get_stats(exact_counter, exact=True)
        self.get_stats(fixed_prob_counter)
        self.get_stats(decr_prob_counter)


    def merge_and_add_dicts(self, dict1, dict2):
        return {k: dict1.get(k, 0) + dict2.get(k, 0) for k in dict1.keys() | dict2.keys()}


    def most_frequent(self, counter, total_top_k_letters):
        return {letter: counter.estimated_events(occur / self.repetitions) for letter, occur in \
            sorted(total_top_k_letters.items(), key=lambda x: x[1], reverse=True)[:self.k]}


    def get_stats(self, counter, exact=False):
        print(counter)

        total_time = 0
        total_events = 0
        total_estimated_events = 0
        total_top_k_letters = {}

        for _ in range(self.repetitions):
            tic = time.time()
            counter.count()
            total_time += time.time() - tic

            if not exact:
                total_events += counter.counter_value
                total_estimated_events += counter.estimated_events()
                total_top_k_letters = self.merge_and_add_dicts(total_top_k_letters, counter.letter_occur)

        avg_time = total_time / self.repetitions

        print(f"\tAverage Counting Time: {avg_time:.2f} seconds")

        if not exact:
            avg_events = total_events / self.repetitions
            estimated_avg_events = total_estimated_events / self.repetitions
            common_top_k_letters = self.most_frequent(counter, total_top_k_letters)

            print(f"\tAverage Counted Events: {avg_events}")
            print(f"\tAverage Estimated Number of Events: {estimated_avg_events}")
            print(f"\tMost Frequent Top {self.k} Letters:")
            [print(f"\t\tAverage Events of the Letter '{letter}': {occur}") for letter, occur in common_top_k_letters.items()]
            print()
            return 

        print(f"\tCounted Events: {counter.counter_value}")
        print(f"\tTop {self.k} Letters:")
        [print(f"\t\tAverage Events of the Letter '{letter}': {occur}") for letter, occur in counter.top_k_letters(self.k).items()]
        print()