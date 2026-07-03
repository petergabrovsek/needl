import random


class MultiNeedle:
    def __init__(self, width: int, height: int, needle: str, needle_count: int, seed: int | None):
        self.width: int = width
        self.height: int = height
        self.haystack: dict[tuple[int, int], str | None] = {(i, j): None for i in range(width) for j in range(height)}

        self.needle: list[str] = list(needle.upper())
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

    def get_directions(self):
        directions = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if i != 0 or j != 0]
        self.random.shuffle(directions)
        return directions

    def place_needles(self, count: int) -> bool:
        # Place needle_count needles in an unambiguous manner
        if count == 0:
            return True

        for x, y in self.free_positions:
            if self.place_needle_2(x, y, self.needle):
                return self.place_needles(count - 1)

        return False

    def place_needle_2(self, x: int, y: int, needle: list[str]) -> bool:
        if len(needle) == 1:
            self.haystack[x, y] = needle[0]
            self.free_positions.remove((x, y))
            self.needles_placed += 1

            as_expected = self.is_solution_count_expected()
            if not as_expected:
                self.haystack[x, y] = None
                self.needles_placed -= 1
                self.free_positions.append((x, y))

            return as_expected

        if self.haystack[x, y] is not None:
            raise Exception(f"Haystack not free at the given position {(x, y)}")

        n, *eedle = needle
        self.haystack[x, y] = n
        self.free_positions.remove((x, y))

        if n == self.first_letter:
            self.first_letter_positions.add((x, y))

        for xx, yy in [(x + dx, y + dy) for dx, dy in self.get_directions()]:
            if not self.is_valid_position(xx, yy) or self.haystack[xx, yy] is not None:
                continue

            placement_successful = self.place_needle_2(xx, yy, eedle)
            if placement_successful:
                return True
            else:
                pass

        self.haystack[x, y] = None
        self.free_positions.append((x, y))
        if n == self.first_letter:
            self.first_letter_positions.remove((x, y))
        return False

    def place_needle(self, x: int, y: int, needle: list[str]) -> bool:
        if len(needle) == 0:
            return True

        is_last_letter = len(needle) == 1
        if is_last_letter:
            self.needles_placed += 1

        n, *eedle = needle
        is_first_letter = n == self.first_letter
        self.haystack[x, y] = n

        if is_first_letter:
            self.first_letter_positions.add((x, y))

        if not self.is_solution_count_expected():
            self.haystack[x, y] = None
            if is_first_letter:
                self.first_letter_positions.remove((x, y))
            if is_last_letter:
                self.needles_placed -= 1
            return False

        neighbours = [(x + dx, y + dy) for dx, dy in self.get_directions()]
        self.random.shuffle(neighbours)
        for neighbour in neighbours:
            if not self.is_valid_position(*neighbour) or self.haystack[neighbour] is not None:
                continue

            placement_successful = self.place_needle(*neighbour, eedle)
            if placement_successful:
                print("Deleted free position 3:", neighbour)
                self.free_positions.remove(neighbour)
                return True

        self.haystack[x, y] = None
        if is_first_letter:
            self.first_letter_positions.remove((x, y))
        if is_last_letter:
            self.needles_placed -= 1
        return False

    def is_solution_count_expected(self) -> bool:
        found_needles = 0
        for x, y in self.first_letter_positions:
            needle_count = self.count_needles(x, y, self.needle)
            if needle_count > 1:
                return False
            found_needles += needle_count

        return found_needles == self.needles_placed

    def count_needles(self, x: int, y: int, needle: list[str]) -> int:
        if len(needle) == 0:
            return 1

        n, *eedle = needle
        if self.haystack[x, y] != n:
            return 0
        elif len(eedle) == 0:
            return 1

        e, *edle = eedle

        self.haystack[x, y] = None

        needle_count = 0
        for xx, yy in [(x + dx, y + dy) for dx, dy in self.get_directions()]:
            if self.is_valid_position(xx, yy) and e == self.haystack[xx, yy]:
                needle_count += self.count_needles(xx, yy, eedle)

        self.haystack[x, y] = n

        return needle_count

    def is_valid_position(self, x: int, y: int):
        """Check if the position is within grid bounds."""
        return 0 <= y < self.height and 0 <= x < self.width

    def print_haystack(self):
        for y in range(self.height):
            for x in range(self.width):
                value = self.haystack[x, y]
                if value is not None:
                    print(self.haystack[x, y], end=' ')
                else:
                    print('.', end=' ')

            print()
        print()
