"""
Main module of kbwl
"""
import argparse
import sys
import itertools

COMMON_NUMBERS = (
    "0", "00",
    "1", "11",
    "12", "21",
    "9", "99",
    "66", "666",
    "2000", "2001", "2002", "2003",
    "2004", "2005", "2006", "2007",
    "2008", "2009", "2010", "2011",
    "2012", "2013", "2014", "2015",
    "2016", "2017", "2018", "2019",
    "2020", "2021", "2022", "2023",
    "2024"
)

COMMON_SYMBOLS = (
    "!", "!!",
    "$", "$$",
    "%", "%%",
    "&", "&&",
    "*", "**",
    "_", "__",
    "-", "--",
    "@", "@@",
    "#", "##",
    "~", "~~"
)

counter: int = 0
wordlist = []


def write_and_log(text):
    """
    Write the text and log the counter on the screen
    """
    global counter  # pylint: disable=global-statement
    wordlist.append(text)
    counter += 1
    print(f"\rGenerating wordlist... {counter}", end="", file=sys.stderr)


def write_pass(namespace, stream, additional):
    """
    Write a single pass, trying all permutations
    """
    for entry in set(itertools.permutations(namespace.keyword)):
        # Write in a few formats:
        # Title case with spaces
        write_and_log(" ".join(entry).title() + additional)
        # Title case with no spaces
        write_and_log("".join(entry).title() + additional)
        # Title case with dots
        write_and_log(".".join(entry).title() + additional)
        # Lower case with spaces
        write_and_log(" ".join(entry).lower() + additional)
        # Lower case with no spaces
        write_and_log("".join(entry).lower() + additional)
        # Lower case with dots
        write_and_log(".".join(entry).lower() + additional)
        # Unchanged case with spaces
        write_and_log(" ".join(entry) + additional)
        # Unchanged case with no spaces
        write_and_log("".join(entry) + additional)
        # Unchanged case with dots
        write_and_log(".".join(entry) + additional)
    stream.flush()


def main():
    """
    Main function of kbwl
    """
    global wordlist  # pylint: disable=global-statement
    parser = argparse.ArgumentParser(
        description="Keyword Based Word List generator")
    parser.add_argument("keyword", nargs="+", action="store",
                        help="List of keywords to generate a wordlist from")
    parser.add_argument("--output", "-o", action="store",
                        default="wordlist.txt",
                        help="File to write output to")
    parser.add_argument("--numbers", "-n", action="store_true",
                        help="Add commonly added numbers")
    parser.add_argument("--symbols", "-s", action="store_true",
                        help="Add commonly added symbols")
    parser.add_argument("--combined", "-c", action="store_true",
                        help="Combine common numbers, symbols")
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.combined:
        print("Warning: Combined mode creates significantly larger wordlists",
              file=sys.stderr)
        namespace.numbers = True
        namespace.symbols = True
    print("Generating wordlist...", end="", file=sys.stderr)
    with open(namespace.output, "w", encoding="utf-8") as stream:
        # First permutation of all keywords
        write_pass(namespace, stream, "\n")
        if namespace.numbers:
            for number in COMMON_NUMBERS:
                write_pass(namespace, stream, f"{number}\n")
        if namespace.symbols:
            for symbol in COMMON_SYMBOLS:
                write_pass(namespace, stream, f"{symbol}\n")
        if namespace.combined:
            for number in COMMON_NUMBERS:
                for symbol in COMMON_SYMBOLS:
                    write_pass(namespace, stream, f"{number}{symbol}\n")
                    write_pass(namespace, stream, f"{symbol}{number}\n")
        print("\nSorting and de-duplicating the wordlist...", end="")
        new_wordlist = sorted(set(wordlist))
        del wordlist  # Free the memory
        print(len(new_wordlist))
        for entry in new_wordlist:
            stream.write(entry)
