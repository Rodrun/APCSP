"""
Minesweeper game.
"""
import os
import argparse

import pygame

import util
from grid import Grid


class Minesweeper(object):

    # The default font to use
    DEFAULT = "Comic Sans MS" if os.name == "nt" else "Arial"

    def __init__(self, rows, cols, w, font=None, font_ratio=0.6,
                 dwidth=800, dheight=600, fit=False, bomb_path="bomb.png",
                 uncover_path="cell_uncover.png", cover_path="cell_cover.png",
                 flag_path="flag.png", bomb_chance=4, bomb_limit=10):
        """
        Initialize pygame and setup minesweeper. Invalid images may raise.
        Arguments:
        rows - Number of rows.
        cols - Number of columns.
        w - Width of a cell.
        font - Font to use. Value of None uses DEFAULT font.
        font_ratio - Font size ratio relative to w. ONLY used if font is None.
        dwidth - Display width.
        dheight - Display height.
        fit - Set the display dimensions to the grid dimensions.
        bomb_path - Path to bomb image.
        uncover_path - Path to uncovered cell image.
        cover_path - Path to covered cell image.
        flag_path - Path to flag image.
        bomb_limit - Maximum amount of bombs allowed.
        bomb_chance - Chance of a cell being a bomb. 4 would be 25%.
        remaining - The remaining cells that need to be cleared.
        """
        self.rows = rows
        self.cols = cols
        self.w = w
        self.detect_end = True  # Detect for win/loss?
        self.bomb_chance = bomb_chance
        self.bomb_limit = bomb_limit
        self.remaining = (rows * cols) - bomb_limit
        self.lost = False  # Track win/loss state
        self.end = False  # Indicator of end of game
        self.end_callbacks = []  # List of callbacks to invoke after game end
        self.after_click = []  # List of callbacks to invoke after a click
        self.revealed_bombs = 0  # Track revealed bombs, when game ends.

        pygame.init()
        pygame.display.set_caption("Minesweeper")
        pygame.display.set_icon(util.load_scaled("icon.png", (32, 32)))

        # Load shared resources
        Grid.font = font
        if font is None:
            Grid.font = pygame.font.SysFont(Minesweeper.DEFAULT,
                                            int(w * font_ratio))

        Grid.bomb_img = util.load_scaled(bomb_path, (w, w))
        Grid.uncover_img = util.load_scaled(uncover_path, (w, w))
        Grid.cover_img = util.load_scaled(cover_path, (w, w))
        Grid.flag_img = util.load_scaled(flag_path, (w - 12, w - 12))

        # Init grid
        self.grid = Grid(rows, cols, w, bomb_chance, bomb_limit)

        if fit:
            dwidth = rows * w
            dheight = cols * w

        self.gameDisplay = pygame.display.set_mode((dwidth, dheight))

    def update(self) -> bool:
        """
        Perform default logical updates for the game.
        Returns:
        False if pygame.QUIT is recieved, True otherwise.
        """
        # Check for game end
        if self.end:
            print("Minesweeper end game detected.")
            self._invoke_end(self.end_callbacks)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.grid.for_each(self._detect_click, event)

        self.grid.update()
        return True

    def _detect_click(self, cell, event):
        """
        Default callback to detect if a bomb was clicked.
        Arguments:
        cell - Cell object.
        Returns:
        True until cell is clicked.
        """
        if event.pos[0] > cell.x \
                and event.pos[0] < cell.x + self.w \
                and event.pos[1] > cell.y \
                and event.pos[1] < cell.y + self.w:
            if event.button == 1:
                cell.action(self._after_action)
                if cell.bomb:
                    self.end_game(True)
                else:
                    self.remaining -= 1
                    print("Remaining cells: ", self.remaining)

                if self.remaining <= 0:
                    self.end_game(False)
            elif event.button == 3:
                cell.flag()
            return False
        return True

    # Callbacks:
    def _show_all_bombs(self, cell):
        """
        Reveal (but do not end game) all bombs. Callback.
        Arguments:
        cell - Cell object.
        Returns:
        True for the entire loop.
        """
        if cell.bomb:
            cell.action()  # Should not end game
        return True

    def _click_all_remaining(self, cell, dry=True):
        """
        For test purposes. Callback to click all remaining cells
        that are not bombs.
        Arguments:
        cell - Cell object.
        dry - True = game win is desired (remaining count is modified).
        Returns:
        True for entire loop.
        """
        if not cell.bomb:
            cell.action(self._after_action)
        if not dry:
            self.remaining = 0  # To provoke reset afterwards
        return True

    def _click_a_bomb(self, cell):
        """
        For test purposes. Callback to click the first encountered bomb.
        Arguments:
        cell - Cell object.
        Returns:
        True until bomb is found.
        """
        if cell.bomb:
            cell.action()
            return False
        return True

    def _after_action(self, cell):
        """
        Default after valid cell action callback. "Valid" meaning the cell
        was not revealed or flagged yet. Only reduces remaining count.
        Arguments:
        cell - Cell object action is performed on successfully.
        """
        self.remaining -= 1
        print("_after_action remaining: ", self.remaining)

    def end_game(self, lost: bool):
        self.lost = lost
        self.end = True
        self._invoke_end(self.end_callbacks, reset=True)

    def set_end_callbacks(self, cb: list):
        """
        Set the list of callbacks that are invoked at the end of
        a game.
        Arguments:
        cb - Callback list.
        """
        self.end_callbacks = cb

    def quit(self):
        """
        Quit pygame.
        """
        pygame.quit()

    def draw(self):
        """
        Draw the grid.
        """
        self.grid.draw(self.gameDisplay)

    def _invoke_end(self, cb: list, reset=True):
        """
        Invoke callbacks on end of game. End of game is when either a bomb was
        clicked on (loss), or no more unrevealed cells remain (win).
        Arguments:
        cb - List of callbacks to invoke in order. Only parameter is remaining
             cell count.
        reset - Reset automatically after invoking callbacks?
        """
        for callback in cb:
            callback(self.remaining)

        if reset:
            self.reset()

    def click_cell(self, i, j):
        """
        Call an action at cell (i, j).
        Returns:
        Generator of integer values of the grid after action.
        """
        self.grid.at(i, j).action(self._after_action)
        return self.get_grid_vals()

    def reset(self):  # TODO: Finish working on this
        """
        Creates a new Grid object to be used when game is reset.
        """
        self.end = False
        self.grid = Grid(self.rows, self.cols, self.w,
                         bomb_chance=self.bomb_chance,
                         bomb_limit=self.bomb_limit)

    def get_grid_vals(self):
        """
        Get a grid value generator to feed to the network.
        Returns:
        Generator of integer values of the grid.
        """
        for c in self.grid:
            yield c.value

    def set_click_callable(self, cb: list):
        """
        Set the list of callbacks to call after a cell action.
        Arguments:
        cb - List of callbacks.
        """
        self.after_action = cb

    @staticmethod
    def arg_parser():
        """
        Get an ArgumentParser instance with useful flags.
        Returns:
        ArgumentParser.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("--no-fit",
                            action="store_false",
                            help="disable window fitting to grid")
        parser.add_argument("--width",
                            type=int,
                            default=800,
                            help="set window width")
        parser.add_argument("--height",
                            type=int,
                            default=600,
                            help="set window height")
        parser.add_argument("--cellw",
                            type=int,
                            help="set cell width",
                            default=50)
        parser.add_argument("--griddim",
                            nargs=2,
                            type=int,
                            metavar=("ROWS", "COLS"),
                            default=[9, 9],
                            help="set grid dimensions")
        parser.add_argument("--chance",
                            type=int,
                            default=4,
                            help="set bomb_chance")
        parser.add_argument("--bombs",
                            type=int,
                            default=10,
                            help="set bomb_limit")
        return parser

    @classmethod
    def from_args(cls):
        """
        Create Minesweeper object from flags on initialization.
        Returns:
        Minesweeper.
        """
        parser = Minesweeper.arg_parser()
        args = parser.parse_args()
        return Minesweeper(rows=args.griddim[0],
                           cols=args.griddim[1],
                           w=args.cellw,
                           fit=args.no_fit,
                           dwidth=args.width,
                           dheight=args.height,
                           bomb_chance=args.chance,
                           bomb_limit=args.bombs)


# If file run as script, e.g. python minesweeper.py
if __name__ == "__main__":
    minesweeper = Minesweeper.from_args()

    running = True
    while running:
        running = minesweeper.update()
        minesweeper.draw()
        pygame.display.flip()
    minesweeper.quit()
