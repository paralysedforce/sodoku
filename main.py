import sys
import numpy as np

from sodoku import Sodoku, get_subsquare

def read_puzzle(filename):
    puzzle = np.zeros((9, 9), dtype=int)
    with open(filename) as f:
        for row, line in enumerate(f.readlines()):
            puzzle[row, :] = np.array([int(num) for num in line.split()],
                    dtype=int)

    return puzzle

def main():
    puzzle = read_puzzle(sys.argv[1])
    sodoku = Sodoku(puzzle)
    print(sodoku)
    sodoku.solve()

if __name__ == '__main__':
    main()
