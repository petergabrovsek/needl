from random import randint
from random import shuffle

class Needl:
    # Directions for 8 neighbors: up, down, left, right, and 4 diagonals
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),  # top row
        (0, -1),           (0, 1),   # middle row (left, right)
        (1, -1),  (1, 0),  (1, 1)    # bottom row
    ]
    
    def __init__(self, width: int, height: int, needle: str):
        self.width = width
        self.height = height
        self.grid: dict[tuple[int, int], str | None] = {(i, j): None for i in range(height) for j in range(width)}
        self.needle = needle

        while True:
            self.initialize_grid()
            if self.fill_grid_randomly():
                self.print_grid()
                break

    def initialize_grid(self):
        row: int = randint(0, self.height - 1)
        column: int = randint(0, self.width - 1)
        self.try_placing_needle(row, column)

        # Check if the grid is solvable before filling
        while self.check_unsolvable_positions():
            # Regenerate the needle
            self.grid = {(i, j): None for i in range(self.height) for j in range(self.width)}
            row = randint(0, self.height - 1)
            column = randint(0, self.width - 1)
            self.try_placing_needle(row, column)

    def try_placing_needle(self, row, column):
        while True:
            self.place_needle(self.needle, row, column)
            if self.count_all_needles() == 1:
                break
            self.grid = {(i, j): None for i in range(self.height) for j in range(self.width)}
            row = randint(0, self.height - 1)
            column = randint(0, self.width - 1)

    def is_valid(self, row, col):
        """Check if the position is within grid bounds."""
        return 0 <= row < self.height and 0 <= col < self.width

    def place_needle(self, needle: str, row: int, col: int) -> bool:
        """Place the needle on the grid."""
        if needle == "":
            # We successfully placed the needle
            return True

        self.grid[row, col] = needle[0]

        # Find all free neighbors for the next letter
        free_neighbours = self.find_free_neighbours(row, col)
        shuffle(free_neighbours)
        for neighbour in free_neighbours:
            result = self.place_needle(needle[1:], neighbour[0], neighbour[1])
            if result:
                return True

        # If we couldn't place the needle, backtrack
        self.grid[row, col] = None
        return False

    def count_needles_at_position(self, needle: str, row: int, col: int) -> int:
        """Find all needles in the grid."""
        if len(needle) == 0:
            return 1
        count = 0
        for direction in self.DIRECTIONS:
            new_row = row + direction[0]
            new_col = col + direction[1]
            if not self.is_valid(new_row, new_col):
                continue
            if self.grid[new_row, new_col] == needle[0]:
                self.grid[new_row, new_col] = None
                count += self.count_needles_at_position(needle[1:], new_row, new_col)
                self.grid[new_row, new_col] = needle[0]
        return count

    def count_all_needles(self) -> int:
        """Find all needles in the grid."""
        needle_count = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row, col] == self.needle[0]:
                    result = self.count_needles_at_position(self.needle[1:], row, col)
                    if result > 0:
                        needle_count += result
                        
        return needle_count

    def find_free_neighbours(self, row: int, col: int) -> list[tuple[int, int]]:
        """Find all free neighbors for the given position."""
        free_neighbours = []
        for direction in self.DIRECTIONS:
            new_row = row + direction[0]
            new_col = col + direction[1]
            if self.is_valid(new_row, new_col) and self.grid[new_row, new_col] is None:
                free_neighbours.append((new_row, new_col))
        return free_neighbours

    def check_unsolvable_positions(self) -> bool:
        """Check if there are any free positions where all possible letters result in more than one needle.
        Returns True if the grid is unsolvable (needle needs to be regenerated)."""
        letters = list(set(self.needle))
        free_positions = [(row, col) for row in range(self.height) for col in range(self.width) if self.grid[row, col] is None]
        
        for row, col in free_positions:
            # Try each possible letter at this position
            all_letters_fail = True
            for letter in letters:
                # Temporarily place the letter
                self.grid[row, col] = letter
                needle_count = self.count_all_needles()
                # Clear the letter
                self.grid[row, col] = None
                
                # If at least one letter works (results in exactly 1 needle), this position is solvable
                if needle_count == 1:
                    all_letters_fail = False
                    break
            
            # If all letters result in more than 1 needle, the grid is unsolvable
            if all_letters_fail:
                return True
        
        return False

    def fill_grid_randomly(self):
        letters = list(set(self.needle))

        free_positions = [(row, col) for row in range(self.height) for col in range(self.width) if self.grid[row, col] is None]
        shuffle(free_positions)

        letters_copy = letters.copy()
        shuffle(letters_copy)
        stack: list[tuple[tuple[int, int], list[str]]] = [(free_positions.pop(), letters_copy)]

        max_iterations = self.width * self.height * 10
        iterations = 0
        while iterations < max_iterations:
            iterations += 1
            position = stack[-1][0]
            row, col = position
            current_letters = stack[-1][1]
                
            if not current_letters:
                # Add the previous position back to free_positions BEFORE popping
                previous_position = stack[-1][0]
                free_positions.append(previous_position)
                stack.pop()
                self.grid[row, col] = None
                if len(stack) == 0:
                    return False
                continue

            self.grid[row, col] = current_letters.pop()
            if self.count_all_needles() > 1:
                continue

            if free_positions:
                # Successfully placed a letter. If there are more positions to fill, add the next one to the stack
                shuffled_letters = letters.copy()
                shuffle(shuffled_letters)
                stack.append((free_positions.pop(), shuffled_letters))
            else:
                # If no free positions left, we're done - all positions are filled
                return True
        # Too many iterations
        return False

    def print_grid(self):
        """Print the grid in a readable format."""
        for row in range(self.height):
            for col in range(self.width):
                cell = self.grid[row, col]
                print('.' if cell is None else cell, end=' ')
            print("")
