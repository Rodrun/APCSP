"""
Grid Object
"""
import pygame

from cell import Cell
from random import randint


class Grid(pygame.sprite.Group):

    bomb_img = None  # Bomb image
    font = None  # Cell font

    def __init__(self, rows, cols, w=50, bomb_chance=4):
        """
        Generate a 2D list of safe and bomb cells.

        Arguments:
        rows - Number of rows.
        cols - Number of columns.
        w - Width of a cell.
        bomb_chance - Chance of a cell being a bomb.
        """
        super().__init__()
        self.rows = rows
        self.cols = cols

        Cell.bomb_img = Grid.bomb_img
        Cell.font = Grid.font
        Cell.cover_img = Grid.cover_img
        Cell.uncover_img = Grid.uncover_img

        # Create grid
        self.array = [[None for i in range(cols)] for j in range(rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                # Determine if bomb
                bomb = True if randint(0, bomb_chance) == 1 else False
                # Create cell
                self.array[i][j] = Cell(bomb, i, j, w)

        for i in range(self.rows):
            for j in range(self.cols):
                current = self.at(i, j)
                self.get_neighbors(current)
                self.set_touching(current)
                self.add(current)  # Add to group

    def get_neighbors(self, cell):
        """
        Add neighboring cells for the cell.surrounding list.

        Arguments:
        cell - Cell to detect neighbors with.
        """
        for a in range(-1, 2):
            for b in range(-1, 2):
                c = cell.i + a
                d = cell.j + b
                if c > -1 and c < self.rows and d > -1 and d < self.cols:
                    # neighbor = grid[c][d]
                    # grid[cell.i][cell.j].surrounding.insert(0, neighbor)
                    neighbor = self.at(c, d)
                    self.at(cell.i, cell.j).surrounding.insert(0, neighbor)

    def at(self, i, j):
        """
        Get cell at (i, j).

        Arguments:
        i - X index.
        j - Y index.
        """
        return self.array[i][j]

    def set_touching(self, c: Cell):
        """
        Get the total amount of touching bomb cells and assign to cell
        member 'touching'.

        Arguments:
        c - Cell to use.

        Returns:
        -1 if bomb, otherwise None.
        """
        if c.bomb:
            return -1
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                a = i + c.i
                b = j + c.j
                if a > -1 and a < self.rows and b > -1 and b < self.cols:
                    neighbor = self.array[a][b]
                    if neighbor.bomb:
                        total = total + 1
        c.touching = total
