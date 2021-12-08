import sys

def open_file(fname, option="r"):
    try:
        return open(fname, option)
    except FileNotFoundError:
        print(f"The file {fname} does not exist")
        sys.exit(1)