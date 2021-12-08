import sys
import logging
import argparse
from exact_counter import ExactCounter
from fixed_prob_counter import FixedProbCounter
from decr_prob_counter import DecreasingProbCounter


class Main:
    def __init__(self):
        fname = self.check_arguments()
        self.exact_counter = ExactCounter(fname)
        self.fixed_counter = FixedProbCounter(fname)
        self.decreasing_counter = DecreasingProbCounter(fname)

        self.handle_results()


    def usage(self):
        print("Usage: python3 main.py\
            \n\t-f <File Name for Counting Letters: str>")
        sys.exit()


    def check_arguments(self):
        arg_parser = argparse.ArgumentParser(
            prog="Approximate Counter",
            usage=self.usage
        )
        arg_parser.add_argument('-help', action='store_true')
        arg_parser.add_argument('-file_name', nargs=1, type=str, default=['datasets/it_book.txt'])

        try:
            args = arg_parser.parse_args()
        except:
            self.usage()

        if args.help:
            self.usage()

        return args.file_name[0]
    

    def handle_results(self):
        logging.info(self.exact_counter.letter_occur)
        logging.info(self.fixed_counter.letter_occur)
        logging.info(self.decreasing_counter.letter_occur)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    main = Main()