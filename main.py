import argparse
from needl import Needl


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find a needle in a haystack grid")
    parser.add_argument("width", type=int, help="Width of the grid")
    parser.add_argument("height", type=int, help="Height of the grid")
    parser.add_argument("needle", type=str, help="The needle (word) to find in the grid")
    
    args = parser.parse_args()
    
    # Ensure needle is uppercase
    needle = args.needle.upper()
    width = args.width
    height = args.height
    
    print(needle.upper(), end='\n\n')

    needl = Needl(width, height, needle)
