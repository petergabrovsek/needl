import json
import random
from pathlib import Path

from svg_grid import grid_to_svg


class MultiNeedle:
    def __init__(self, width: int, height: int, needle: str, needle_count: int, seed: int | None):
        self.width: int = width
        self.height: int = height
        self.haystack: dict[tuple[int, int], str | None] = {}

        self.needle_word: str = needle.upper()
        self.needle: list[str] = list(self.needle_word)
        self.letters: list[str] = sorted(list(set(self.needle)))
        self.needle_count: int = needle_count
        self.needles_placed: int = 0

        self.random = random
        if seed is not None:
            self.random.seed(seed)

        self.free_positions: list[tuple[int, int]] = []
        self.used_positions: list[tuple[int, int]] = []

        self.first_letter = self.needle[0]
        self.first_letter_positions: set[tuple[int, int]] = set()
        self.paths: list[list[tuple[int, int]]] = []

    def generate(self) -> bool:
        max_tries = 10
        while max_tries > 0:
            max_tries -= 1
            self.initialize_haystack()
            paths = self.place_needles(self.needle_count)
            if paths is not None and self.fill_haystack():
                self.paths = paths
                grid_to_svg(self.width, self.height, self.paths, self.needle_word)
                return True
        return False

    def initialize_haystack(self):
        self.haystack = {(i, j): None for i in range(self.width) for j in range(self.height)}
        self.paths = []
        self.needles_placed = 0
        self.free_positions = [(i, j) for i in range(self.width) for j in range(self.height)]
        self.random.shuffle(self.free_positions)
        self.first_letter_positions = set()

    def get_directions(self):
        directions = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if i != 0 or j != 0]
        self.random.shuffle(directions)
        return directions

    def place_needles(self, count: int) -> list[list[tuple[int, int]]] | None:
        # Place needle_count needles in an unambiguous manner
        if count == 0:
            return []

        for x, y in self.free_positions:
            path = self.place_needle(x, y, self.needle)
            if path is not None:
                remaining_paths = self.place_needles(count - 1)
                if remaining_paths is not None:
                    return [path] + remaining_paths

        return None

    def place_needle(self, x: int, y: int, needle: list[str]) -> list[tuple[int, int]] | None:
        if len(needle) == 1:
            self.haystack[x, y] = needle[0]
            self.free_positions.remove((x, y))
            self.needles_placed += 1

            as_expected = self.is_solution_count_expected()
            if not as_expected:
                self.haystack[x, y] = None
                self.needles_placed -= 1
                self.free_positions.append((x, y))
                return None

            return [(x, y)]

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

            path = self.place_needle(xx, yy, eedle)
            if path:
                return [(x, y)] + path

        self.haystack[x, y] = None
        self.free_positions.append((x, y))
        if n == self.first_letter:
            self.first_letter_positions.remove((x, y))
        return None

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

        self.haystack[x, y] = None

        needle_count = 0
        for xx, yy in [(x + dx, y + dy) for dx, dy in self.get_directions()]:
            if self.is_valid_position(xx, yy) and eedle[0] == self.haystack[xx, yy]:
                needle_count += self.count_needles(xx, yy, eedle)

        self.haystack[x, y] = n

        return needle_count

    def fill_haystack(self) -> bool:
        letters = self.letters.copy()
        self.random.shuffle(letters)

        # TODO: replace the tuple with the named tuple
        stack: list[tuple[tuple[int, int], list[str]]] = [(self.free_positions.pop(), letters)]

        max_iterations = self.width * self.height * len(self.needle) * 2
        iterations = 0
        while iterations < max_iterations:
            iterations += 1
            position = stack[-1][0]
            remaining_letters = stack[-1][1]

            if not remaining_letters:
                previous_position = stack[-1][0]
                self.free_positions.append(previous_position)
                stack.pop()
                letter = self.haystack[position]
                self.haystack[position] = None
                if letter == self.first_letter:
                    self.first_letter_positions.remove(position)
                if len(stack) == 0:
                    return False
                continue

            letter = remaining_letters.pop()
            self.haystack[position] = letter
            if letter == self.first_letter:
                self.first_letter_positions.add(position)
            if not self.is_solution_count_expected():
                continue

            if self.free_positions:
                letters = self.letters.copy()
                self.random.shuffle(letters)
                stack.append((self.free_positions.pop(), letters))
            else:
                return True

        return False

    def is_valid_position(self, x: int, y: int):
        """Check if the position is within grid bounds."""
        return 0 <= y < self.height and 0 <= x < self.width

    def haystack_to_grid(self) -> list[list[str | None]]:
        return [
            [self.haystack[x, y] for x in range(self.width)]
            for y in range(self.height)
        ]

    @staticmethod
    def grid_to_haystack(grid: list[list[str | None]]) -> dict[tuple[int, int], str | None]:
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0
        return {
            (x, y): grid[y][x]
            for y in range(height)
            for x in range(width)
        }

    def to_dict(self) -> dict:
        return {
            "width": self.width,
            "height": self.height,
            "haystack": self.haystack_to_grid(),
            "needle": self.needle_word,
            "needle_count": self.needle_count,
            "paths": [[[x, y] for x, y in path] for path in self.paths],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MultiNeedle":
        obj = cls(
            data["width"],
            data["height"],
            data["needle"],
            data["needle_count"],
            seed=None,
        )
        obj.haystack = cls.grid_to_haystack(data["haystack"])
        obj.paths = [[tuple(point) for point in path] for path in data["paths"]]
        obj.needles_placed = len(obj.paths)
        obj.first_letter_positions = {
            (x, y)
            for x in range(obj.width)
            for y in range(obj.height)
            if obj.haystack[x, y] == obj.first_letter
        }
        return obj

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, data: str) -> "MultiNeedle":
        return cls.from_dict(json.loads(data))

    def save_json(self, path: str | Path, **kwargs) -> None:
        Path(path).write_text(self.to_json(**kwargs), encoding="utf-8")

    @classmethod
    def load_json(cls, path: str | Path) -> "MultiNeedle":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

    def print_haystack(self):
        for y in range(self.height):
            for x in range(self.width):
                value = self.haystack[x, y]
                if value is not None:
                    print(self.haystack[x, y], end=' ')
                elif (x, y) in self.free_positions:
                    print(' ', end=' ')
                else:
                    print('-', end=' ')

            print()
        print()
