from decr_prob_counter import DecreasingProbCounter
from exact_counter import ExactCounter
from fixed_prob_counter import FixedProbCounter
import time
from math import sqrt
from tabulate import tabulate
import matplotlib.pyplot as plt


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


    def calc_mean(self, letter_occur):
        return sum(letter_occur.values()) / len(letter_occur)


    def calc_variance(self, letter_occur, mean):
        dvts = [(x - mean) ** 2 for x in letter_occur.values()]
        return sum(dvts) / len(letter_occur)


    def get_stats(self, counter, exact_counter=False):
        print(f"{counter}\n")

        total_time, total_means, total_countings, total_estimated_events,\
            total_std_dvt, total_variance, total_min_events, total_max_events =\
                0, 0, 0, 0, 0, 0, 0, 0
        total_top_k_letters = {}
        plot_data = [[], [], []]

        for i in range(self.rep):
            tic = time.time()
            counter.count()
            total_time += time.time() - tic


            if not exact_counter:
                counter.estimate_events()
                total_countings += sum(counter.letter_occur.values())
                total_estimated_events += sum(counter.estimated_letter_occur.values())
                total_min_events += min(counter.estimated_letter_occur.values())
                total_max_events += max(counter.estimated_letter_occur.values())

                mean = self.calc_mean(counter.estimated_letter_occur)
                variance = self.calc_variance(counter.estimated_letter_occur, mean)
                std_dvt = sqrt(variance)

                total_means += mean
                total_variance += variance
                total_std_dvt += std_dvt
                total_top_k_letters = self.merge_and_add_dicts(total_top_k_letters, counter.estimated_letter_occur)

                rep = i + 1
                plot_data[0].append(rep)
                plot_data[1].append(abs(self.total_events - (total_estimated_events / rep)) / self.total_events * 100)
                plot_data[2].append(abs(self.std_dvt - (total_std_dvt / rep)) / self.std_dvt * 100)


        avg_time = round(total_time / self.rep, 3)
        data = [["Counting Time (s)", avg_time], ["Events"], ["Mean"], ["Minimum"], ["Maximum"], ["Variance"], ["Standard Deviation"]]
        headers = ["Measure", "Value"]
        
        if exact_counter:
            self.exact_top_k_letters = counter.top_k_letters(self.k)
            self.k = len(self.exact_top_k_letters)
            self.alphabet_size = len(counter.letter_occur)
            self.total_events = total_countings = sum(counter.letter_occur.values())
            self.mean = mean = self.calc_mean(counter.letter_occur)
            self.min_events = min_events = min(counter.letter_occur.values())
            self.max_events = max_events = max(counter.letter_occur.values())
            self.variance = variance = self.calc_variance(counter.letter_occur, mean)
            self.std_dvt = std_dvt = sqrt(variance)
            data[1].append(round(self.total_events, 2))
            data[2].append(round(self.mean, 2))
            data[3].append(round(self.min_events, 2))
            data[4].append(round(self.max_events, 2))
            data[5].append(round(self.variance, 2))
            data[6].append(round(self.std_dvt, 2))
        else:
            headers.extend(["Absolute Error", "Relative Error (%)"])
            total_countings = round(total_countings / self.rep, 2)
            total_events = round(total_estimated_events / self.rep, 2)
            mean = round(total_means / self.rep, 2)
            min_events = round(total_min_events / self.rep, 2)
            max_events = round(total_max_events / self.rep, 2)
            variance = round(total_variance / self.rep, 2)
            std_dvt = round(total_std_dvt / self.rep, 2)
            common_top_k_letters = self.most_frequent(total_top_k_letters)

            data[1].extend([total_events, round(abs(self.total_events - total_events), 2),
                round(abs(self.total_events - total_events) / self.total_events * 100, 2)])
            data[2].extend([mean, round(abs(self.mean - mean), 2),
                round(abs(self.mean - mean) / self.mean * 100, 2)])
            data[3].extend([min_events, round(abs(self.min_events - min_events), 2),
                round(abs(self.min_events - min_events) / self.min_events * 100, 2)])
            data[4].extend([max_events, round(abs(self.max_events - max_events), 2),
                round(abs(self.max_events - max_events), 2) / round(self.max_events * 100, 2)])
            data[5].extend([variance, round(abs(self.variance - variance), 2),
                round(abs(self.variance - variance) / self.variance * 100, 2)])
            data[6].extend([std_dvt, round(abs(self.std_dvt - std_dvt), 2),
                round(abs(self.std_dvt - std_dvt) / self.std_dvt * 100, 2)])
        

        print(f"Results for {self.rep} repetition{'s' if self.rep != 1 else ''}:")
        print(f"Total Elapsed Time: {round(total_time, 3)} s\nTotal Events Counted: {total_countings}")
        print("\nAverage Values for a Repetition:")
        print(tabulate(data, headers=headers))

        print(f"\nTop {self.k} Most Frequent Letters:")
        if exact_counter:
            [print(f"\tEvents of the Letter '{letter}': {occur}") for letter, occur in self.exact_top_k_letters.items()]
        else:
            relative_precision, right_position_letters = 0, 0
            exact_top_k_letters = list(self.exact_top_k_letters.keys())

            for i, letter_occur in enumerate(common_top_k_letters.items()):
                letter, occur = letter_occur
                if letter == exact_top_k_letters[i]:
                    right_position_letters += 1
                    relative_precision += right_position_letters / (i + 1)
                print(f"\tEvents of the Letter '{letter}': {occur}")
            
            avg_relative_precision = relative_precision / self.k * 100
            TP = len([letter for letter in common_top_k_letters.keys() if letter in self.exact_top_k_letters.keys()])
            FP = self.k - TP
            TN = self.alphabet_size - self.k - FP
            precision = TP / self.k * 100
            accuracy = (TP + TN) / self.alphabet_size * 100

            # recall not appropriate since we are evaluation a top n frequent letters
            print(f"\n\tPrecision: {precision:.2f} %")
            print(f"\tAccuracy: {accuracy:.2f} %")
            print(f"\tAverage Precision (relative order): {avg_relative_precision:.2f} %")
            
            plt.plot(plot_data[0], plot_data[1], label="Total Events Relative Error")
            plt.plot(plot_data[0], plot_data[2], label="Standard Deviation Relative Error")
            plt.title(counter)
            plt.legend()
            plt.show()

        print("\n")
