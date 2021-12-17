import sys

def open_file(fname, option="r", encoding='utf-8'):
    try:
        return open(fname, option, encoding=encoding)
    except FileNotFoundError:
        print(f"The file {fname} does not exist")
        sys.exit(1)