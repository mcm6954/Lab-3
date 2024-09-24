"""
CSAPX Lab 3: Tripods

A program that finds the optimal placement of a number of tripods in a grid
of numbers.  A tripod can touch three adjacent cells, based on orientation,
e.g. a north facing tripod touches the east, south and west cells.

The goal is to find the placement of a number of tripods, such that the
total sums of the cells that all combined tripods touch is maximum.

Usage: python3 tripods.py filename

Author: Mia McSwain
"""
import sys
from dataclasses import dataclass

import combi_sort

"""
Tripod:
    row (int): Row the tripod is placed
    col (int): Column the tripod is placed
    orient (str): Orientation of the tripod
    total (int): Total sum of the tripod's legs
"""
@dataclass (frozen = True)
class Tripod:
    row: int
    col: int
    orient: str
    total: int

def read_data(filename : str) -> list:
    """
    Scans the given file, arranging the given values into a 2D array
    :param filename: The file to be scanned
    :return: The specified 2D array
    """
    with open(filename) as f:
        size = f.readline().strip().split(' ')
        rows = int(size[0])
        #columns = int(size[1])
        grid = []
        for i in range(rows):
            nums = []
            c = f.readline().strip().split(' ')
            for w in c:
                nums.append(int(w))
            grid.append(nums)
    return grid

def print_grid(grid : list) -> None:
    """
    Prints the given 2D array if it's not too large. If it is too large, prints a message stating such
    :param grid: The 2D array that should be printed
    :return: None
    """
    print('Rows: {} Columns: {}'.format(len(grid), len(grid[0])))
    if len(grid) <= 50 and len(grid[0]) <= 30:
        for r in grid:
            result = ''
            for c in range(len(r)):
                result += str(r[c]) + ' '
            print(result)
    else:
        result = 'Too large to print!'
        print(result)

def possible_tripods(grid : list, requested_tri : int) -> bool:
    """
    Determines if the requested number of tripods for a grid is possible for its size
    :param grid: 2D Array that the possible tripods will be determined from
    :param requested_tri: The requested number of tripods to be placed
    :return: Returns true if the grid CAN have the requested number of tripods. Returns false otherwise
    """
    r = len(grid)
    c = len(grid[0])
    if (r*c - 4) < requested_tri:
        print('Too many tripods!')
        return False
    else:
        return True

def compute_orientation(grid: list, row: int, column: int) -> str:
    """
    Computes orientation for tripods along the edge of the grid, and leaves the orientation open for those in the center
    :param grid: 2D Array that the tripods reference
    :param row: Row of tripod
    :param column: Column of tripod
    :return: If along the edge of the grid, returns the only possible direction. Otherwise, returns an empty string.
    """
    if row == 0:
        return 'SOUTH'
    elif row == len(grid)-1:
        return 'NORTH'
    elif column == 0:
        return 'EAST'
    elif column == len(grid[row])-1:
        return 'WEST'
    else:
        return ''

def compute_sum(grid: list, r: int, c: int, o: str) -> int:
    """
    Computes the sum of the tripod's legs based on the tripod's orientation
    :param grid: 2D Array that the tripods reference
    :param r: Row of tripod
    :param c: Column of tripod
    :param o: Orientation of tripod
    :return: Returns total sum of tripod's legs
    """
    north_num = grid[r-1][c]
    if len(grid) > r+1:
        south_num = grid[r+1][c]
    else:
        south_num = 0
    west_num = grid[r][c-1]
    if len(grid[r]) > c+1:
        east_num = grid[r][c+1]
    else:
        east_num = 0
    total = 0
    if o == 'SOUTH':
        total = west_num + south_num + east_num
    elif o == 'NORTH':
        total = west_num + north_num + east_num
    elif o == 'WEST':
        total = north_num + west_num + south_num
    elif o == 'EAST':
        total = north_num + east_num + south_num
    return total

def compute_tripods(grid : list) -> list:
    """
    Computes the possible and best tripod for each grid position, adding them to a list
    :param grid: 2D Array that the tripods reference
    :return: Returns a list of tripods
    """
    tripods = []
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            # skip corners
            if (r == 0 and c == 0) or (r == 0 and c == cols-1) or \
                (r == rows-1 and c == 0) or (r == rows-1 and c == cols-1):
                continue
            # interior cells
            elif compute_orientation(grid, r, c) == '':
                best = Tripod(
                        row=r,
                        col=c,
                        orient=str('NORTH'),
                        total=int(compute_sum(grid, r, c, 'NORTH')))
                east = Tripod(
                    row=r,
                    col=c,
                    orient=str('EAST'),
                    total=int(compute_sum(grid, r, c, 'EAST')))
                if east.total > best.total:
                    best = east
                south = Tripod(
                    row=r,
                    col=c,
                    orient=str('SOUTH'),
                    total=int(compute_sum(grid, r, c, 'SOUTH')))
                if south.total > best.total:
                    best = south
                west = Tripod(
                        row=r,
                        col=c,
                        orient=str('WEST'),
                        total=int(compute_sum(grid, r, c, 'WEST')))
                if west.total > best.total:
                    best = west
                tripods.append(best)
            # edge cells
            else:
                tripods.append(Tripod(
                    row=r,
                    col=c,
                    orient=str(compute_orientation(grid, r, c)),
                    total=int(compute_sum(grid, r, c, compute_orientation(grid, r, c)))))
    return tripods


def main() -> None:
    """
    The main function
    :return: None
    """
    if len(sys.argv) < 2:
        print('Usage: python3 tripods.py filename')
    else:
        grid = read_data(sys.argv[1])
        print_grid(grid)
        tri_num =int(input('Number of tripods: '))
        if possible_tripods(grid, tri_num) == True:
            print('Optimal placement:')
            tripods = compute_tripods(grid)
            tripods = combi_sort.combi_sort(tripods)
            tripods.reverse()
            total_sum = 0
            for i in range(tri_num):
                print('location: ({},{}), orientation: {}, sum: {}'.format(tripods[i].row, tripods[i].col, tripods[i].orient, tripods[i].total))
                total_sum += tripods[i].total
            print('Total sum:',total_sum)



if __name__ == '__main__':
    main()
