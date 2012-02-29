#! /bin/env python
"""
Author: Christopher Mitchell <chris@chrismitchell.name>
Date: 2011-09
Description: This program provides a fast and simple textual interface for
    using elementary row-operations to manipulate matrices. Besides the row
    operations, interesting features include undo and log printing. Use the
    command '?' for a listing of all commands.
"""

from operator import mul, add
from copy import deepcopy
from fractions import Fraction
import sys

class Matrix(object):
    def __init__(self, n, k):
        """Create a zero-filled matrix with `n` equations and `k` unknowns."""
        self.n = n
        self.k = k
        self.mat = [[Fraction(i*n+j) for j in range(k)] for i in range(n)]

    def __str__(self):
        """Return a human-readable display of the matrix values."""
        strings = [[str(self.mat[i][j]) for j in range(self.k)] for i in
                range(self.n)]
        str_width = max([max(len(elem) for elem in row) for row in strings])

        result = ""
        format_string = "{{:>{}}}".format(str_width+1)
        for idx, row in enumerate(strings):
            result += "R{} ".format(idx+1)
            for elem in row:
                result += format_string.format(elem)
            result += "\n"
        return result[:-1]

    def __repr__(self):
        return repr(self.mat)

    def copy(self):
        return deepcopy(self)

    @classmethod
    def _mult_row(cls, row, scalar):
        """Return the result of multiplying `row` by `scalar`."""
        return map(mul, row, [scalar] * len(row))

    @classmethod
    def _add_rows(cls, row_a, row_b):
        """Return the result of summing `row_a` and `row_b`."""
        return map(add, row_a, row_b)

    def swap(self, a, b):
        """Swap rows `a` and `b`."""
        a -= 1
        b -= 1
        self.mat[a], self.mat[b] = self.mat[b], self.mat[a]

    def mult(self, a, scalar):
        """Multiply row `a` by `scalar`."""
        a -= 1
        self.mat[a] = Matrix._mult_row(self.mat[a], scalar)

    def add(self, scalar, a, b):
        """Add `scalar` times row `a` to row `b`."""
        a -= 1
        b -= 1
        summand = Matrix._mult_row(self.mat[a], scalar)
        self.mat[b] = Matrix._add_rows(summand, self.mat[b])


def modifies(fn):
    """
    A decorator used to tag CLI commands that will modify the current matrix.
    The CLI uses this information to decide when to re-print the matrix.
    """
    fn.modifies = True
    return fn

def help_text(help_text):
    """
    A decorator to tag CLI commands with text that explains the tagged command's
    purpose. The help text for every command is displayed to the user by the
    help command.
    """
    def deco(fn):
        fn.help_text = help_text
        return fn
    return deco

class CLI(object):
    """
    This command line interface lets users interactively modify a matrix
    (internally, a Matrix instance) and does some other special things, like
    keeping an undo stack.
    """
    def __init__(self):
        """
        Create a dormant CLI. To start it asking for input, call `run_console`.
        """
        self.mat = Matrix(4, 4)

        # used to keep a pristine copy of newly-created matrices so that users
        # can revert to its original state
        self.start = self.mat

        # head of the undo stack is the state right before the current one
        self.undo_stack = []
        # head of the log stack is natural description of the operation done to
        # the last state to yield the current state.
        self.log_stack = []

        self.commands_with_key = []
        self.commands_by_key = {}
        self.register('n', self.new)
        self.register('s', self.swap)
        self.register('m', self.mult)
        self.register('a', self.add)
        self.register('u', self.undo)
        self.register('r', self.revert)
        self.register('p', self.display)
        self.register('l', self.print_log)
        self.register('?', self.command_info)
        self.register('q', self.quit)

    @help_text("show a log of your changes to the current matrix")
    def print_log(self):
        if len(self.log_stack) == 0:
            print "No logs to print."
            return

        for i in range(len(self.undo_stack)):
            print self.log_stack[i]
            print self.undo_stack[i]
            print
        # Recall that the last log message corresponds to the operation that
        # produced the current matrix.
        print self.log_stack[-1]
        print self.mat

    def register(self, key, fn):
        """
        Register the command/key `key` to execute `func` and save internally
        useful help text and data about whether or not the function modifies
        the matrix.
        """
        self.commands_with_key.append((fn, key))
        self.commands_by_key[key] = fn

    @modifies
    @help_text("create a new matrix")
    def new(self):
        print "Create a matrix with n rows and k columns."
        try:
            n = int(raw_input("How many rows? "))
            k = int(raw_input("How many columns? "))
        except ValueError:
            print "! Oops! Please try again, inputting integers."
            return 0

        mat = Matrix(n, k)

        print ("Enter your data one row at a time, separating the numbers with spaces.")
        for row_idx in range(n):
            numbers = []
            while True:
                user_input = raw_input("R{}: ".format(row_idx+1))
                try:
                    numbers = [Fraction(num.strip()) for num in
                            user_input.strip().split(" ")]
                except ValueError:
                    print "! Could not parse your input as numbers."
                    continue
                if len(numbers) != k:
                    print "! You entered {} numbers, but the system expects {}. Please try again.".format(len(numbers), k)
                    continue
                else:
                    break
            mat.mat[row_idx] = numbers

        self.undo_stack = []
        self.log_stack = ["Create a new {} by {} matrix.".format(n, k)]
        self.start = mat.copy()
        self.mat = mat
        return 1

    @modifies
    @help_text("revert the matrix to its original state")
    def revert(self):
        self.undo_stack = []
        self.log_stack = []
        self.mat = self.start
        return 1

    @modifies
    @help_text("swap one row for another")
    def swap(self):
        print "Swap two rows."
        try:
            row_a = int(raw_input("Row A: "))
            row_b = int(raw_input("Row B: "))
        except ValueError:
            print "! Your input was not understood. Try the row number by itself."
            return 0
        self.undo_stack.append(self.mat.copy())
        self.log_stack.append("Swap R{} with R{}".format(row_a, row_b))
        self.mat.swap(row_a, row_b)
        return 1

    @modifies
    @help_text("multiply a row by some value")
    def mult(self):
        print "Multiply a row."
        try:
            row = int(raw_input("Row: "))
            multiplier = Fraction(raw_input("Multiplier: "))
        except ValueError:
            print "! Your input was not understood. Please try again."
            return 0
        self.undo_stack.append(self.mat.copy())
        self.log_stack.append("Multiply R{} by {}".format(row, multiplier))
        self.mat.mult(row, multiplier)
        return 1
        
    @modifies
    @help_text("add a multiple of one row to another row")
    def add(self):
        print "Add n times row A to row B."
        try:
            multiplier = Fraction(raw_input("Multiplier: "))
            row_a = int(raw_input("Row A: "))
            row_b = int(raw_input("Row B: "))
        except ValueError:
            print "! Your input did not look like numbers."
            return 0
        else:
            if not (1 <= row_a <= self.mat.k) or not (1 <= row_b <= self.mat.k):
                print "! Invalid row number."
                return 0
        self.undo_stack.append(self.mat.copy())
        self.log_stack.append("Add {} times R{} to R{}".format(
            multiplier, row_a, row_b))
        self.mat.add(multiplier, row_a, row_b)
        return 1

    @help_text("show the current matrix")
    def display(self):
        print self.mat

    @modifies
    @help_text("undo the latest change to the matrix")
    def undo(self):
        try:
            self.mat = self.undo_stack.pop()
            self.log_stack.pop()
            return 1
        except IndexError:
            print "! No change to undo."
            return 0

    @help_text("show this list of commands and their descriptions")
    def command_info(self):
        for fn, key in self.commands_with_key:
            print "  {} - {}".format(key, fn.__dict__.get("help_text", ""))

    @help_text("quit the program")
    def quit(self):
        sys.exit(0)

    def run_console(self):
        """Start the interactive console."""
        print "Use the '?' command for help."
        while True:
            try:
                key = raw_input("> ")
            except (KeyboardInterrupt, EOFError):
                print
                self.quit()

            try:
                cmd = self.commands_by_key[key]
            except KeyError:
                print "That command is unrecognized. Try '?' for help."
                print
                continue

            success = cmd()
            if success and cmd.modifies:
                print 
                print "Result:"
                print self.mat
            print


if __name__ == "__main__":
    t = CLI()
    t.run_console()
