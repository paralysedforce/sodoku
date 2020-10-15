import numpy as np

class Sodoku():
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self._possibilities = {}
        self.solved = False


    def __str__(self):
        horizontal_bar = "." + ("-" * 23) + "." + "\n"
        row_template = "| {0} {1} {2} | {3} {4} {5} | {6} {7} {8} |\n"

        ret = horizontal_bar
        for i, row in enumerate(self.puzzle):
            ret += row_template.format(*[val if val else " " for val in row])

            if i % 3 == 2:
                ret += horizontal_bar
        return ret


    def validate(self):
        return check_rows(self.puzzle) and \
            check_cols(self.puzzle) and \
            check_subsquares(self.puzzle)

    def _find_all_possibilities(self):
        for i in range(9):
            for j in range(9):
                self._update_possibilities(i, j)

    def _update_possibilities(self, row, col):
        if self.puzzle[row, col]:
            self._possibilities[(row, col)] = []

        else:
            non_possiblities = set()
            for val in self.puzzle[row, :]:
                non_possiblities.add(val)

            for val in self.puzzle[:, col]:
                non_possiblities.add(val)

            for val in get_subsquare(self.puzzle, row // 3, col // 3):
                non_possiblities.add(val)

            self._possibilities[(row, col)] = [
                    i for i in range(1, 10)
                    if i not in non_possiblities]

    def solve(self):
        solving = True
        self._find_all_possibilities()

        while solving:
            solving = False
            for row, col in self._possibilities:
                possibilities = self._possibilities[(row, col)]
                if len(possibilities) == 1:
                    solving = True
                    self.puzzle[row, col] = possibilities[0]
                    self._find_all_possibilities()
                    print(self)
                    input()

        if 0 not in self.puzzle.flatten():
            self.solved = True

        print(self)


def get_rows(puzzle):
    for row in puzzle:
        yield row


def get_cols(puzzle):
    for col in puzzle.T:
        yield col


def get_subsquares(puzzle):
    for row in range(3):
        for col in range(3):
            yield get_subsquare(puzzle, row, col)

def get_subsquare(puzzle, row, col):
    return puzzle[3*row:(3*(row+1)), 3*col: 3*(col+1)].flatten()


def validation_generator(gen):
    def wrapped(puzzle):
        for section in gen(puzzle):
            if duplicate_numbers(section):
                return False
        return True
    return wrapped


check_rows = validation_generator(get_rows)
check_cols = validation_generator(get_cols)
check_subsquares = validation_generator(get_subsquares)

def duplicate_numbers(section):
    int_section = [int(num) for num in section if num]
    return len(set(int_section)) < len(int_section)
