import random


class MultiNeedle:
    DIRECTIONS = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if i != 0 or j != 0]

    def __init__(self, width: int, height: int, needle: str, needle_count: int, seed: int | None):
        self.width: int = width
        self.height: int = height
        self.haystack: dict[tuple[int, int], str | None] = {(i, j): None for i in range(width) for j in range(height)}

        self.needle: str = needle.upper()
        self.letters: set[str] = set(self.needle)
        self.needle_count: int = needle_count
        self.needles_placed: int = 0

        self.random = random
        if seed is not None:
            self.random.seed(seed)

        self.free_positions: list[tuple[int, int]] = [(i, j) for i in range(width) for j in range(height)]
        self.random.shuffle(self.free_positions)
        self.used_positions: list[tuple[int, int]] = []

        self.first_letter = self.needle[0]
        self.first_letter_positions: set[tuple[int, int]] = set()

        self.place_needles(needle_count)

    def place_needles(self, count: int) -> bool:
        print(count)
        # Place needle_count needles in an unambiguous manner
        if count == 0:
            return True

        x, y = self.free_positions.pop()
        self.place_needle(x, y, list(self.needle))

        # while not self.place_needle(x, y, list(self.needle)):
        #     if len(self.free_positions) == 0:
        #         print("NO FREE POSITIONS")
        #         return False
        #     x, y = self.free_positions.pop()

        self.print_haystack()

        return self.place_needles(count - 1)

    def place_needle(self, x: int, y: int, needle: list[str]) -> bool:
        if len(needle) == 0:
            return True
        elif len(needle) == 1:
            self.needles_placed += 1

        print(needle, self.needles_placed)

        n, *eedle = needle
        is_first_letter = n == self.first_letter
        self.haystack[x, y] = n

        if is_first_letter:
            self.first_letter_positions.add((x, y))

        solution_count = self.is_solution_count_expected(needle)
        print("solution count as expected:", solution_count)
        if not solution_count:
            self.haystack[x, y] = None
            if is_first_letter:
                self.first_letter_positions.remove((x, y))
            print(solution_count)
            return False

        neighbours = [(x + dx, y + dy) for dx, dy in self.DIRECTIONS]
        self.random.shuffle(neighbours)
        for neighbour in neighbours:
            if self.haystack[neighbour] is not None:
                continue

            placement_successful = self.place_needle(*neighbour, eedle)
            if placement_successful:
                return True

        self.haystack[x, y] = None
        if is_first_letter:
            self.first_letter_positions.remove((x, y))
        return False

    def is_solution_count_expected(self, needle: list[str]) -> bool:
        found_needles = 0
        print("first letter positions:", self.first_letter_positions)
        for x, y in self.first_letter_positions:
            needle_count = self.count_needles(x, y, needle)
            if needle_count > 1:
                self.print_haystack()
                return False
            found_needles += needle_count

        self.print_haystack()
        print("found", found_needles, "placed", self.needles_placed)
        return found_needles == self.needles_placed

    def count_needles(self, x: int, y: int, needle: list[str]) -> int:
        if len(needle) == 0:
            print("needle count '0'", needle)
            return 1

        n, *eedle = needle

        needle_count = 0
        print(self.DIRECTIONS)
        for xx, yy in [(x + dx, y + dy) for dx, dy in self.DIRECTIONS]:
            if self.is_valid_position(xx, yy) and self.haystack[xx, yy] == n:
                print("Detected correct letter")
                needle_count += self.count_needles(xx, yy, eedle)
        print("needle count", needle, needle_count)

        return needle_count

    def is_valid_position(self, row, col):
        """Check if the position is within grid bounds."""
        return 0 <= row < self.height and 0 <= col < self.width

    def print_haystack(self):
        for y in range(20):
            for x in range(20):
                value = self.haystack[x, y]
                if value is not None:
                    print(self.haystack[x, y], end=' ')
                else:
                    print('.', end=' ')

            print()
        print("\n" * 5)

