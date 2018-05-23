"""
Minesweeper game environment. Can be used as an OpenAI Gym environment.

Controls:
    F5: Show all revealable cells (dry).
    F6: Show all bombs & disable lose.
    F7: Reset.
    F8: Show all cell debug coordinates.

Observation space (Box, 3 dimensions/channels):
Representative of an image of the grid.

Action Spcae (Discrete):
NUM     ACTION
0       Click cell 0
...n-1  Click cell n-1

Reward:
For every solve: 2.
For every click on a non-revealed cell: 1.
For every click on a revealed cell: -1.
For every click on a bomb: -2.
"""
import os
import argparse

from PIL import Image
import numpy as np
import pygame
from gym import spaces, Env

from . import util
from .grid import Grid
# from grid_space import GridSpace


class Minesweeper(Env):

    # For gym.Env
    metadata = {"render.modes": ["human"]}
    # The default font to use
    DEFAULT = "Comic Sans MS" if os.name == "nt" else "Arial"

    def __init__(self, rows, cols, w, font=None, font_ratio=0.6,
                 dwidth=800, dheight=600, fit=True, bomb_path="bomb.png",
                 uncover_path="cell_uncover.png", cover_path="cell_cover.png",
                 flag_path="flag.png", bomb_chance=4, bomb_limit=10,
                 user_input=True, dbg_reveal=False, reveal_dry=True):
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
        user_input - Allow user input.
        dbg_reveal - Reveal all cells? Calls _click_all_remaining().
        reveal_dry - 'dry' parameter for _click_all_remaining().
        """
        self.rows = rows
        self.cols = cols
        self.w = w
        self.user_input = user_input
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

        if fit:
            dwidth = rows * w
            dheight = cols * w
        self.dwidth = dwidth
        self.dheight = dheight

        self.gameDisplay = pygame.display.set_mode((dwidth, dheight))

        # Init grid
        self.reset()
        self.update()
        self.draw()

        if dbg_reveal:
            self.grid.for_each(self._click_all_remaining, reveal_dry)

        # See module docstring for info
        # self.action_space = spaces.Tuple([spaces.Discrete(self.cols),
        #                                   spaces.Discrete(self.rows)])
        self.action_space = spaces.Discrete(self.cols * self.rows)
        self.observation_space = spaces.Box(low=0,
                                            high=255,
                                            shape=(dheight, dwidth, 3))

    TEMP = "TEMP.png"

    def _get_obs(self):
        """
        Get the current observation space. It is an image grab of the grid
        surface.
        Returns:
        Updated observation space.
        """
        obs = np.array(Image.frombytes("RGB",
                                       self.gameDisplay.get_rect().size,
                                       self.gameDisplay.get_buffer().raw))
        print("Observation shape: ", obs.shape)
        return obs

    # For gym.Env:
    def step(self, action):
        """
        Derived from gym.Env.
        Returns:
        observation, reward, done, info - Tuple.
        """
        print(action)
        assert self.action_space.contains(action)
        cx, cy = self._get_action_coords(action)
        # Check if cell already revealed
        c_revealed = self.grid.at(cx, cy).revealed

        # Perform action
        self.click_cell(cx, cy)

        # Check if lost/won
        self.update()  # Ctrl + C will force end
        self.draw()
        done = self.end
        if done:
            if self.lost:
                print("Game lost")
                reward = -1.0  # Punish lost
            else:
                print("Game won")
                reward = 2.0  # Reward solve
        else:
            if c_revealed:  # Cell already clicked
                reward = -1.0  # Punish uselessness
                done = True
            else:
                reward = 1.0  # Reward valid action

        observation = self._get_obs()
#        info = {"remaining": self.remaining,
#                "action": (cx, cy),
#                "raw action": action}
        return observation, reward, done, {}

    def _get_action_coords(self, action):
        """
        Get I and J coordinates of action.
        Arguments:
        action - Action input from step().
        Returns:
        I and J integers.
        """
        return self.grid.get_by_id(action).location

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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F5:
                    self.grid.for_each(self._show_all_bombs)
                elif event.key == pygame.K_F6:
                    self.grid.for_each(self._click_all_remaining)
                elif event.key == pygame.K_F7:
                    self.end_game(False)
                elif event.key == pygame.K_F8:
                    self.grid.for_each(self._show_cell_debug)

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
        # Detect if user input allowed
        if not self.user_input:
            return False

        if event.pos[0] > cell.x \
                and event.pos[0] < cell.x + self.w \
                and event.pos[1] > cell.y \
                and event.pos[1] < cell.y + self.w:
            if event.button == 1:
                cell.action(self._after_action)

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
        dry - False = game win is desired (remaining count is modified).
        Returns:
        True for entire loop.
        """
        if not cell.bomb:
            cell.action(self._after_action if not dry else None)
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
            cell.action(self._after_action)
            return False
        return True

    def _show_cell_debug(self, cell):
        """
        Callback to show coordinates of each covered cell.
        Arguments:
        cell - Cell object.
        Returns:
        True for entire loop.
        """
        cell.enable_debug()
        return True

    def _after_action(self, cell):
        """
        Default after valid cell action callback. "Valid" meaning the cell
        was not revealed or flagged yet. Only reduces remaining count.
        Arguments:
        cell - Cell object action is performed on successfully.
        """
        # print(cell)
        if cell.bomb and not cell.flagged:
            self.end_game(True)  # Lose game
            return
        if not cell.revealed and not cell.flagged:
            self.remaining -= 1
        # Detect game win
        if self.remaining <= 0:
            self.end_game(False)

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

    # Env inheritance
    def render(self, mode="human"):
        """
        Derived from gym.Env.
        """
        self.draw()

    def draw(self, flip=True):
        """
        Draw the grid and optionally flip the display.
        """
        self.grid.draw(self.gameDisplay)
        if flip:
            pygame.display.flip()

    def _invoke_end(self, cb: list, reset=True):
        """
        Invoke callbacks on end of game. End of game is when either a bomb was
        clicked on (loss), or no more unrevealed cells remain (win).
        Arguments:
        cb - List of callbacks to invoke in order. Parameters given are:
             cell count and lost bool.
        reset - Reset automatically after invoking callbacks?
        """
        for callback in cb:
            callback(self.remaining, self.lost)

        if reset:
            self.reset()

    def click_cell(self, i, j):
        """
        Call an action at cell (i, j).
        Arguments:
        i - Column.
        j - Row.
        Returns:
        Generator of integer values of the grid after action.
        """
        print("Cell click at ", self.grid.at(i, j).coordinates())
        self.grid.at(i, j).action(self._after_action)
        return self.get_grid_vals()

    def reset(self):
        """
        Creates a new Grid object to be used when game is reset.
        """
        self.end = False
        del self.grid
        self.grid = Grid(self.rows, self.cols, self.w,
                         bomb_chance=self.bomb_chance,
                         bomb_limit=self.bomb_limit)
        self.remaining = self.get_total_cells() - self.bomb_limit
        print("Grid reset. Remaining: ", self.remaining, " ",
              self.grid.state_str())
        self.update()
        self.draw()
        return self._get_obs()

    def get_grid_vals(self):
        """
        Get a grid value generator to feed to the network.
        Returns:
        Generator of integer values of the grid.
        """
        for c in self.grid:
            yield c.get_value()

    def set_click_callbacks(self, cb: list):
        """
        Set the list of callbacks to call after a cell action.
        Arguments:
        cb - List of callbacks.
        """
        self.after_action = cb

    def get_total_cells(self):
        """
        Get total amount of cells in the grid. Wrapper for
        grid.get_total_cells().
        Returns:
        Cell count.
        """
        return self.grid.get_total_cells()

    @staticmethod
    def arg_parser(parser=None):
        """
        Get an ArgumentParser instance with useful flags.
        Arguments:
        parser - If given, will use this parser object and add extra arguments.
                 Note that this could create conflicts with the extra args.
        Returns:
        ArgumentParser.
        """
        if parser is None:
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
        parser.add_argument("--debug-reveal-cells",
                            action="store_true",
                            help="Reveal all non-bomb cells")
        parser.add_argument("--debug-reveal-no-dry",
                            action="store_false",
                            help="Disable dry (no win) reveal when using"
                                 + "--debug-reveal-cells flag?")
        return parser

    @classmethod
    def from_args(cls, parser=None):
        """
        Create Minesweeper object from flags on initialization..
        Arguments:
        parser - If given, will use this parser. NOTE: Will assume that it will
                 have arguments that arg_parser() adds.
        Returns:
        Minesweeper.
        """
        if parser is None:
            parser = Minesweeper.arg_parser()
        args = parser.parse_args()
        return Minesweeper(rows=args.griddim[0],
                           cols=args.griddim[1],
                           w=args.cellw,
                           fit=args.no_fit,
                           dwidth=args.width,
                           dheight=args.height,
                           bomb_chance=args.chance,
                           bomb_limit=args.bombs,
                           dbg_reveal=args.debug_reveal_cells,
                           reveal_dry=args.debug_reveal_no_dry)


# If file run as script, e.g. python minesweeper.py
if __name__ == "__main__":
    minesweeper = Minesweeper.from_args()

    running = True
    while running:
        running = minesweeper.update()
        minesweeper.draw()
    minesweeper.quit()
