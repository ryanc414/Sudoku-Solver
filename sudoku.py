#!/usr/bin/env python
"""
Sudoku solver.

Use: specify sudoku grid in a text file with space-separated digits and the
unknown digits each represented by '0'. Pass the filename as the first arg
to this program when executed.

If no solution can be found, process will be aborted. If a solution can be
found, the completed grid will be printed. This does not guarantee that the
solution is unique however.
"""

from sys import argv

# Import Grid and error handling classes.
from grid import *


class Sudoku(Grid):
    """Represents a Sudoku grid."""
    def __init__(self, grid_file=None):
        """A Sudoku grid is 9x9 and is filled with digits 1-9."""
        self.digits = range(1, 10)
        self.n = 9
        self.quadrants = {0: [0, 1, 2], 1: [3, 4, 5], 2: [6, 7, 8]}
        super(Sudoku, self).__init__(grid_file)

    def check_grid(self):
        """Check that the input grid is a valid Sudoku grid."""
        try:
            # First check that the grid is 9x9.
            assert(self.n_rows == self.n and self.n_cols == self.n)
        except AssertionError:
            raise InvalidGridError("Error, input grid must be 9x9.")
        else:
            # The parent class checks for equal row lengths.
            super(Sudoku, self).check_grid()
            # Next, check that all digits are within the range 0-9.
            self.check_for_invalid_digits()
            # Finally, check for any duplicate digits in rows, columns and
            # quadrants that would make the grid invalid.
            for i in range(self.n):
                self.check_for_row_duplicates(i)
                self.check_for_column_duplicates(i)
            for i in self.quadrants.iterkeys():
                for j in self.quadrants.iterkeys():
                    self.check_for_quadrant_duplicates(i, j)

    def check_for_row_duplicates(self, row):
        """Check for duplicates in specified row."""
        found_digits = set()
        for i in range(self.n):
            if self[i, row] != 0 and self[i, row] in found_digits:
                raise InvalidGridError(
                    "Error, duplicate digits found in row {}.".format(row))
            else:
                found_digits.add(self[i, row])

    def check_for_column_duplicates(self, col):
        """Check for duplicates in specified column."""
        found_digits = set()
        for i in range(self.n):
            if self[col, i] != 0 and self[col, i] in found_digits:
                raise InvalidGridError(
                    "Error, duplicate digits found in column {}.".format(col))
            else:
                found_digits.add(self[col, i])

    def check_for_quadrant_duplicates(self, x, y):
        """Check for duplicates in specified quadrant."""
        found_digits = set()
        for i in self.quadrants[x]:
            for j in self.quadrants[y]:
                if self[i, j] != 0 and self[i, j] in found_digits:
                    raise InvalidGridError(
                        "Error, duplicate digits found in quadrant {}, {}"
                        "".format(x, y))
                else:
                    found_digits.add(self[i, j])

    def check_for_invalid_digits(self):
        """Check for any invalid digits in the grid."""
        for i in range(self.n):
            for j in range(self.n):
                if self[i, j] not in range(self.n):
                    raise InvalidGridError("Error, input grid must contain"
                                           "digits 0-9 only.")

    def solve(self):
        """Completely solve a given input Sudoku."""
        while not self.complete():
            found_one = False
            # Iterate through all elements.
            for i in range(self.n):
                for j in range(self.n):
                    # Check if the digit is known - unknown digits will be 0.
                    if self[i, j] == 0:
                        possible_digits = self.check_possible_digits(i, j)
                        if len(possible_digits) == 1:
                            found_one = True
                            digit, = possible_digits
                            self[i, j] = digit
            # Check if at least one digit has been found on each pass. If not,
            # then no more digits will be found on subsequent passes so the
            # Sudoku grid cannot be solved.
            if not found_one:
                raise Exception("Error, cannot solve.")

    def complete(self):
        """
        Determine whether the Sudoku is complete. A complete Sudoku will
        contain no '0's.
        """
        for i in range(self.n):
            for j in range(self.n):
                if self[i, j] == 0:
                    return False
        return True

    def check_possible_digits(self, i, j):
        """
        For a given grid position, check which digits are allowed to
        be there. A digit is allowed to be there if it is not already
        in the quadrant, row or column.
        """
        digits = set(self.digits)
        self.remove_digits_in_quadrant(digits, i, j)
        self.remove_digits_in_col(digits, i)
        self.remove_digits_in_row(digits, j)
        return digits

    def remove_digits_in_quadrant(self, digits, i, j):
        """
        Remove digits from the set of possibles that are in the same
        quadrant as the element in question.
        """
        col_range = self.quadrant_limits(i)
        row_range = self.quadrant_limits(j)
        for i in col_range:
            for j in row_range:
                digits.discard(self[i, j])

    def quadrant_limits(self, x):
        """Return limiting indices of the current quadrant."""
        for q_range in self.quadrants.itervalues():
            if x in q_range:
                return q_range
        raise IndexError

    def remove_digits_in_col(self, digits, col):
        """
        Remove digits from the set of possibilities that are in the same
        column as the element in question.
        """
        for i in range(self.n):
            digits.discard(self[col, i])

    def remove_digits_in_row(self, digits, row):
        """
        Remove digits from the set of possibilities that are in the same
        row as the element in question.
        """
        for i in range(self.n):
            digits.discard(self[i, row])


if __name__ == '__main__':
    try:
        my_sudoku = Sudoku(argv[1])
    except IOError:
        print "Error, could not read specified file."
    except IndexError:
        print "Error, no input file was specified."
    else:
        my_sudoku.solve()
        my_sudoku.print_grid()
