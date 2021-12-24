from decr_prob_counter import DecreasingProbCounter
from exact_counter import ExactCounter
from fixed_prob_counter import FixedProbCounter
import time
from math import sqrt


class Test():
    def __init__(self, fname="datasets/it_book.txt", rep=1000, k=10):
        self.fname = fname
        self.rep = rep
        self.k = k

        self.run_test()


    def run_test(self):
        exact_counter, fixed_prob_counter, decr_prob_counter =\
            ExactCounter(self.fname), FixedProbCounter(self.fname), DecreasingProbCounter(self.fname)

        self.get_stats(exact_counter, exact_counter=True)
        self.get_stats(fixed_prob_counter)
        self.get_stats(decr_prob_counter)


    def merge_and_add_dicts(self, dict1, dict2):
        return {k: dict1.get(k, 0) + dict2.get(k, 0) for k in dict1.keys() | dict2.keys()}


    def most_frequent(self, total_top_k_letters):
        return {letter: occur for letter, occur in \
            sorted(total_top_k_letters.items(), key=lambda x: x[1], reverse=True)[:self.k]}


    def mean(self, letter_occur):
        return sum(letter_occur.values()) / len(letter_occur)


    def variance(self, letter_occur, mean):
        deviations = [(x - mean) ** 2 for x in letter_occur.values()]
        return sum(deviations) / len(letter_occur)


    def get_stats(self, counter, exact_counter=False):
        print(f"{counter}\n")

        total_time, total_means, total_events, total_estimated_events,\
            total_std_deviation, total_variance, total_min_events, total_max_events =\
                0, 0, 0, 0, 0, 0, 0, 0
        total_top_k_letters = {}

        for _ in range(self.rep):
            tic = time.time()
            counter.count()
            total_time += time.time() - tic

            if not exact_counter:
                counter.estimate_events()
                total_events += sum(counter.letter_occur.values())
                total_estimated_events += sum(counter.estimated_letter_occur.values())
                total_min_events += min(counter.estimated_letter_occur.values())
                total_max_events += max(counter.estimated_letter_occur.values())

                mean = self.mean(counter.estimated_letter_occur)
                variance = self.variance(counter.estimated_letter_occur, mean)
                std_deviation = sqrt(variance)

                total_means += mean
                total_variance += variance
                total_std_deviation += std_deviation
                total_top_k_letters = self.merge_and_add_dicts(total_top_k_letters, counter.estimated_letter_occur)

        avg_time = total_time / self.rep

        if exact_counter:
            self.exact_top_k_letters = counter.top_k_letters(self.k)
            self.k = len(self.exact_top_k_letters)
            self.alphabet_size = len(counter.letter_occur)
        else:
            mean = total_means / self.rep
            min_events = total_min_events / self.rep
            max_events = total_max_events / self.rep
            mean = total_means / self.rep
            variance = total_variance / self.rep
            std_deviation = total_std_deviation / self.rep
            events = total_events / self.rep
            estimated_events = total_estimated_events / self.rep
            common_top_k_letters = self.most_frequent(total_top_k_letters)

            print(f"\tTotal Effected Countings for {self.rep} Repetition{'s' if self.rep != 1 else ''}: {events:.2f}")
            print(f"\tAverages Values for {self.rep} repetition{'s' if self.rep != 1 else ''}:")
            print(f"\t\tCounting Time: {avg_time:.2f} seconds")
            print(f"\t\tTotal Number of Events: {estimated_events:.2f}")
            print(f"\t\tMean: {mean:.2f}")
            print(f"\t\tMinimum: {min_events:.2f}")
            print(f"\t\tMaximum: {max_events:.2f}")
            print(f"\t\tVariance: {variance:.2f}")
            print(f"\t\tStandard Deviation: {std_deviation:.2f}")
            
            print(f"\t\t{'Most Frequent ' if self.rep != 1 else ''}Top {self.k} Letters:")
            relative_precision, right_position_letters = 0, 0
            exact_top_k_letters = list(self.exact_top_k_letters.keys())

            for i, letter_occur in enumerate(common_top_k_letters.items()):
                letter, occur = letter_occur
                if letter == exact_top_k_letters[i]:
                    right_position_letters += 1
                    relative_precision += right_position_letters / (i + 1)
                print(f"\t\t\tEvents of the Letter '{letter}': {occur}")
            
            avg_relative_precision = relative_precision / self.k * 100
            TP = len([letter for letter in common_top_k_letters.keys() if letter in self.exact_top_k_letters.keys()])
            FP = self.k - TP
            TN = self.alphabet_size - self.k - FP
            precision = TP / self.k * 100
            accuracy = (TP + TN) / self.alphabet_size * 100

            # recall not appropriate since we are evaluation a top n frequent letters
            print(f"\t\t\tPrecision: {precision:.2f}%")
            print(f"\t\t\tAccuracy: {accuracy:.2f}%")
            print(f"\t\t\tAverage Precision (relative order): {avg_relative_precision:.2f}%")

            # TODO:
            # compare with exact counter: in terms of absolute and relative errors (lowest value, highest value, average value)

            print("\n")
            return

        mean = self.mean(counter.letter_occur)
        variance = self.variance(counter.letter_occur, mean)
        std_deviation = sqrt(variance)

        print(f"\tTotal Effected Countings for {self.rep} Repetition{'s' if self.rep != 1 else ''}:\
            {sum(counter.letter_occur.values())}")
        print(f"\tAverage Values for {self.rep} repetition{'s' if self.rep != 1 else ''}:")
        print(f"\t\tCounting Time: {avg_time:.2f} seconds")
        print(f"\t\tTotal Number of Events: {sum(counter.letter_occur.values())}")
        print(f"\t\tMean: {mean}")
        print(f"\t\tMinimum: {min(counter.letter_occur.values())}")
        print(f"\t\tMaximum: {max(counter.letter_occur.values())}")
        print(f"\t\tVariance: {variance:.2f}")
        print(f"\t\tStandard Deviation: {std_deviation:.2f}")
        print(f"\t\tTop {self.k} Letters:")
        [print(f"\t\t\tEvents of the Letter '{letter}': {occur}") for letter, occur in self.exact_top_k_letters.items()]

        print("\n")
