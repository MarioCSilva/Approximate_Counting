from decr_prob_counter import DecreasingProbCounter
from exact_counter import ExactCounter
from fixed_prob_counter import FixedProbCounter
import time


class Test():
    def __init__(self, fname="datasets/it_book.txt", rep=1000, k=10):
        self.fname = fname
        self.rep = rep
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


    def most_frequent(self, total_top_k_letters):
        return {letter: occur for letter, occur in \
            sorted(total_top_k_letters.items(), key=lambda x: x[1], reverse=True)[:self.k]}
    

    def mean(self, letter_occur):
        return sum(letter_occur.values()) / len(letter_occur)


    def get_stats(self, counter, exact=False):
        print(f"{counter}\n")

        total_time, total_means, total_events, total_estimated_events = 0, 0, 0, 0
        total_top_k_letters = {}

        for _ in range(self.rep):
            tic = time.time()
            counter.count()
            total_time += time.time() - tic

            if not exact:
                counter.estimate_events()
                total_events += sum(counter.letter_occur.values())
                total_estimated_events += sum(counter.estimated_letter_occur.values())
                total_means += self.mean(counter.estimated_letter_occur)
                total_top_k_letters = self.merge_and_add_dicts(total_top_k_letters, counter.estimated_letter_occur)

        avg_time = total_time / self.rep

        print(f"\t{'Average ' if self.rep != 1 else ''}Counting Time: {avg_time:.2f} seconds")

        if not exact:
            avg_means = total_means / self.rep
            avg_events = total_events / self.rep
            estimated_avg_events = total_estimated_events / self.rep
            common_top_k_letters = self.most_frequent(total_top_k_letters)

            print(f"\tCounted Events: {avg_events:.2f}")
            print(f"\tEstimated Number of Events: {estimated_avg_events:.2f}")
            print(f"\tMean Estimated Number of Events: {avg_means:.2f}")
            
            print(f"\t{'Most Frequent ' if self.rep != 1 else ''}Top {self.k} Letters:")
            [print(f"\t\tEvents of the Letter '{letter}': {occur}") for letter, occur in common_top_k_letters.items()]
            
            print(f"Note: These are Averages Values for {self.rep} repetition{'s' if self.rep != 1 else ''}\n")
            return 

        print(f"\tCounted Events: {sum(counter.letter_occur.values())}")
        print(f"\tNumber of Events: {sum(counter.letter_occur.values())}")
        print(f"\tMean Number of Events: {self.mean(counter.letter_occur)}")
        print(f"\tTop {self.k} Letters:")
        [print(f"\t\tEvents of the Letter '{letter}': {occur}") for letter, occur in counter.top_k_letters(self.k).items()]

        print(f"Note: These are Averages Values for {self.rep} repetition{'s' if self.rep != 1 else ''}\n")
