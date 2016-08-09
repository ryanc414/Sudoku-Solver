#!/usr/bin/env python
"""Classes that assist input and manipulation of number grids."""


class CouldNotConvertInt(Exception):
    """Failure to convert input to integers."""


class InvalidGridError(Exception):
    """Input grid is invalid."""


class Grid(object):
    """Represents a grid of numbers."""
    def __init__(self, grid_file=None):
        self.grid = []
        self.n_rows = 0
        self.n_cols = 0
        if grid_file is not None:
            self.read_gridfile(grid_file)

    def __getitem__(self, item):
        """
        Provides access to grid numbers via self[i, j], representing the
        i^th column and j^th row.
        """
        i, j = item
        return self.grid[j][i]

    def __setitem__(self, key, value):
        """Allows grid values to be set via self[i, j] = value."""
        i, j = key
        self.grid[j][i] = value

    def __len__(self):
        return len(self.grid)

    @staticmethod
    def convert_line_to_int(line_list):
        """
        Converts a list of strings to a list of integers
        """
        try:
            int_list = [int(num) for num in line_list]
            return int_list
        except:
            raise CouldNotConvertInt(format(line_list))

    def read_gridfile(self, grid_file):
        """Reads a grid from file."""
        with open(grid_file) as f:
            self.grid = [
                self.convert_line_to_int((line.strip()).split(' '))
                for line in f
                ]
        self.n_rows = len(self)
        self.n_cols = len(self.grid[0])
        self.check_grid()

    def check_grid(self):
        """Check that each row in the grid has the same length."""
        try:
            for i in range(self.n_rows):
                assert(len(self.grid[i]) == self.n_cols)
        except AssertionError:
            raise InvalidGridError("Error, unequal row lengths in input grid.")

    def print_grid(self):
        """
        Prints a grid from file, for debugging purposes
        """
        for j in range(self.n_rows):
            for i in range(self.n_cols):
                print self[i, j],
            print('\n'),
