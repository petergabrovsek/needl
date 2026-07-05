import argparse
from needl import Needl

from multi_needle import MultiNeedle

import random

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Find a needle in a haystack grid")
    # parser.add_argument("width", type=int, help="Width of the grid")
    # parser.add_argument("height", type=int, help="Height of the grid")
    # parser.add_argument("needle", type=str, help="The needle (word) to find in the grid")
    #
    # args = parser.parse_args()
    #
    # # Ensure needle is uppercase
    # needle = args.needle.upper()
    # width = args.width
    # height = args.height
    #
    # print(needle.upper(), end='\n\n')
    #
    # needl = Needl(width, height, needle)

    random.seed(0)

    words = [
        'banana', 'lomljenka', 'sladoled', 'plezanje', 'poletje',
        'morje', 'nevihta', 'korenje', 'balkon', 'avtodom',
        'magnezij', 'spanje', 'kovanec', 'fotografija', 'aknajlvatses',
    ]

    for i, word in enumerate(words):
        print(word.upper())
        needl = MultiNeedle(30, 42, word, 5, seed=i)
        needl.print_haystack()

    # needl = MultiNeedle(30, 42, "aknajlvatses", random.randint(5, 10), 1)
    # needl.print_haystack()


    # for y in range(20):
    #     for x in range(20):
    #         value = needl.haystack[x, y]
    #         if value is not None:
    #             print(needl.haystack[x, y], end=' ')
    #         else:
    #             print('.', end=' ')
    #
    #     print()

