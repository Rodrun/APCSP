"""Minesweeper grid object.

Keeps cells organized and allows traversal and accessing of thereof.
"""
import numpy as np
import pygame

from .cell import Cell
from random import randint


class Grid(pygame.sprite.Group):

    bomb_img = None  # Bomb image
    font = None  # Cell font

    def __init__(self, rows, cols, w=50, bomb_chance=4, bomb_limit=10,
                 x_offset=0, y_offset=0):
        """
        Generate a 2D list of safe and bomb cells.
        Arguments:
        rows - Number of rows.
        cols - Number of columns.
        w - Width of a cell.
        bomb_chance - Chance of a cell being a bomb. (Deprecated)
        bomb_limit - Amount of bombs.
        """
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.total_bombs = bomb_limit
        self.w = w
        self.bombs = []

        # Ensure no illegal dimensions
        assert rows >= 1
        assert cols >= 1

        Cell.bomb_img = Grid.bomb_img
        Cell.font = Grid.font
        Cell.cover_img = Grid.cover_img
        Cell.uncover_img = Grid.uncover_img
        Cell.flag_img = Grid.flag_img

        # Generate random bomb coordinates
        if bomb_limit <= rows * cols:
            bomb_tuples = set()
            remaining = bomb_limit
            while remaining != 0:
                tx = randint(0, cols-1)
                ty = randint(0, rows-1)
                coord = self._coord_str(tx, ty)
                # Avoid duplicates
                if coord not in bomb_tuples:
                    bomb_tuples.add(self._coord_str(tx, ty))
                    remaining -= 1

        # Create grid
        self.id_table = {}  # For quick lookup
        self.array = [[None for i in range(cols)] for j in range(rows)]
        curr_id = 0
        for j in range(self.rows):  # Row (y)
            for i in range(self.cols):  # Column (x)
                scoord = self._coord_str(i, j)
                self.array[j][i] = Cell(i, j, self.w, curr_id,
                                        bomb=scoord in bomb_tuples)
                # Add to lookup table, but only coordinates (i, j)
                self.id_table[str(curr_id)] = (i, j)
                curr_id += 1

        for j in range(self.rows):
            for i in range(self.cols):
                current = self.at(i, j)
                self.get_neighbors(current)
                self.set_touching(current)
                self.add(current)  # Add to group

    def for_each(self, callback, *args):
        """
        Call callback on each cell.
        Arguments:
        callback - Callback, only argument is the current cell object. False
                   is returned: will break loop.
        args - Any additional arguments that the callback may require.
        """
        for j in self.array:
            for i in j:
                if not callback(i, *args):
                    break

    def get_by_id(self, id):
        """
        Get cell object by ID (numeric string).
        Arguments:
        id - ID to lookup, can be integer or str.
        Returns:
        Cell object if found, otherwise None.
        """
        if str(id) in self.id_table:
            c = self.id_table[str(id)]
            return self.array[c[1]][c[0]]
        else:
            return None

    def get_values(self) -> tuple:
        """
        Get two lists of all cell values.
        Returns:
        Pixel values list 2d.
        """
        # Create empty 2d lists of 0s
        # rr = range(self.rows)
        # cr = range(self.cols)  # Might be redundant but screw it for now:
        # revealed = [[self.at(i, j).get_values()[0] for i in cr] for j in rr]
        # touching = [[self.at(i, j).get_values()[1] for i in cr] for j in rr]
        # # Get values and put them in their respective lists
        # self.for_each(self._update_value_lists, revealed, touching)
        # return revealed, touching
        out = np.zeros(shape=(3, self.rows, self.cols), dtype=np.uint8)
        self.for_each(self._update_color_lists, out)
        return out

    def _update_color_lists(self, cell, out: list):
        """
        Callback to update given output colors list to feed the network.
        Arguments:
        cell - Cell object.
        out - Output list
        Returns:
        True for entire loop.
        """
        out[cell.j][cell.i] = list(Cell.value_to_rgba(cell.get_values()[1]))
        return True

    def _update_value_lists(self, cell, rlist: list, tlist: list):
        """
        Callback to update given value lists.
        Arguments:
        cell - Cell object.
        rlist - Revealed list (must be 2D).
        tlist - Touching list (must be 2D).
        Returns:
        True for entire loop.
        """
        i = cell.i
        j = cell.j
        rlist[j][i], tlist[j][i] = cell.get_values()
        return True

    def get_total_cells(self):
        """
        Get total cells.
        Returns:
        Cell count.
        """
        return self.rows * self.cols

    def state_str(self):
        """
        Get basic overview information about the current
        state of the grid.
        Returns:
        State string.
        """
        return "Grid {}x{}, Bombs: {}, w: {}".format(self.rows, self.cols,
                                                     self.total_bombs, self.w)

    def _coord_str(self, x, y):
        """
        Convert coordinate into a string.
        Arguments:
        x - X coordinate.
        y - Y coordinate.
        Returns:
        Coordinate string.
        """
        return ",".join([str(i) for i in [x, y]])

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

    def detect_click(self, mx, my):
        """
        Detect click on a cell given click coordinates on screen.
        Arguments:
        mx - Mouse X.
        my - Mouse Y.
        """
        pass

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
