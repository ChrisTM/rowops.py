rowops.py
=========
rowops.py is a keyboard-driven interface for manipulating a matrix with the three elementary row operations.

This tool was created for students in a linear algebra course who are doing things like practicing the reduction of a matrix into reduced row echelon form. Using rowops.py is way faster than practicing by hand or with a calculator.


What are some cool features?
----------------------------
  * undo! If you manipulate by mistake, use `u` to undo.
  * a manipulation log. If you worked on a long problem, use `l` to print out all the steps you took to get there.
  * fractions. No ugly decimals. You can use fractions for input too.


How do I use it?
----------------
Run rowops.py by entering `python rowops.py` on your command line. You'll get a console that looks like:

    Use the '?' command for help.
    > 

The `>` symbol means the program is ready for you to start a new command. You can type `?` and hit enter to list all of the available commands. 

    > ?
      n - create a new matrix
      s - swap one row for another
      m - multiply a row by some value
      a - add a multiple of one row to another row
      u - undo the latest change to the matrix
      r - revert the matrix to its original state
      p - show the current matrix
      l - show a log of your changes to the current matrix
      ? - show this list of commands and their descriptions
      q - quit the program


Give me a walkthrough, please.
------------------------------
For practice, you can try creating a new matrix by using the `n` (for new) command. In our example, we create a 3x2 matrix. The process looks like this:

    > n
    Create a matrix with n rows and k columns.
    How many rows? 2
    How many columns? 3
    Enter your data one row at a time, separating the numbers with spaces.
    R1: 1 2 3
    R2: 4 5 6

    Result:
    R1  1 2 3
    R2  4 5 6

Any command that creates or changes a matrix will print out the result. Let's halve the second row with the `m` command. Notice that rowops.py supports fractions!

    > m
    Multiply a row.
    Row: 2
    Multiplier: 1/2

    Result:
    R1    1   2   3
    R2    2 5/2   3

We add -1 times row one to row two...

    > a
    Add n times row A to row B.
    Multiplier: -1
    Row A: 1
    Row B: 2

    Result:
    R1    1   2   3
    R2    1 1/2   0

The last elementary row operation is swapping rows. That's easy:

    > s
    Swap two rows.
    Row A: 1
    Row B: 2

    Result:
    R1    1 1/2   0
    R2    1   2   3

Let's print a log to see all of our great work in one place!

    > l
    Create a new 2 by 3 matrix.
    R1  1 2 3
    R2  4 5 6

    Multiply R2 by 1/2
    R1    1   2   3
    R2    2 5/2   3

    Add -1 times R1 to R2
    R1    1   2   3
    R2    1 1/2   0

    Swap R1 with R2
    R1    1 1/2   0
    R2    1   2   3
