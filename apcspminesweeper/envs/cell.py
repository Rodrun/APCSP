"""Grid cell object.

Take note that a cell object has no reset function, meaning a reset
must be done by deletion and recreation of a Cell object. Cell object
coordinates are represented as: (i, j), where i is the X and j is the Y
relative to the position in the grid array.S
"""
import copy

import pygame

from .util import font_scaled


class Cell(pygame.sprite.Sprite):

    bomb_img = None  # Bomb image
    cover_img = None  # Unclicked image
    uncover_img = None  # Revealed image
    font = None  # Font to display # touching bombs
    RGB_GRAY = [90, 90, 90, 255]

    def __init__(self, x, y, w, id, bomb=False, rows=9, cols=9):
        """
        Arguments:
        bomb - Is bomb?
        x - X location in grid.
        y - Y location in grid.
        w - Width of cell.
        id - ID of cell.
        rows - Rows of parent grid.
        cols - Columns of parent grid.
        """
        super().__init__()
        self.i = x  # Grid coordinate X
        self.j = y  # Grid coordinate Y
        self.location = (self.i, self.j)  # Nice tuple
        self.x = x * w  # Display coordinate X
        self.y = y * w  # Dispaly coordinate Y
        self.w = w
        self.id = id
        self._set_image(Cell.cover_img)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.bomb = bomb
        self.revealed = False
        self.flagged = False
        self.touching = 0
        self.rows = rows
        self.cols = cols
        self.actDebounce = False
        self.surrounding = []
        self.tagged = False
        self.rendered_text = False  # To prevent Font.render() multiple times
        self.rendered_debug = False  # ^ but for coordinate display on cell
        self.show_debug = False  # Show debug coordinates over cell?
        # print(self.get_summary())

    def __repr__(self):
        return self.get_summary()

    def update(self):
        if self.revealed:
            if self.bomb:
                self._set_image(Cell.bomb_img)
            else:
                if not self.rendered_text:  # Create text image only once
                    self._set_image(Cell.uncover_img)
                    if self.touching != 0:
                        text = Cell.font.render(str(self.touching),
                                                True,
                                                (255, 0, 0))
                    else:
                        text = None
                    if text is not None:
                        self.image.blit(text, (self.w * .3, self.w * .1))
                    self.rendered_text = True
        elif not self.revealed and self.flagged:
            self._set_image(Cell.flag_img)
        else:  # Covered cell
            # Debug coordinates
            if self.show_debug:
                if not self.rendered_debug:
                    # Create coordinate text
                    txt = font_scaled(str((self.i, self.j)),
                                      Cell.font,
                                      (self.w, self.w),
                                      (0, 255, 0))
                    self.rendered_debug = True  # Prevent repeated rendering
                else:
                    txt = None
                # Draw coordinates
                if txt is not None:
                    self.image.blit(txt, (0, 0))
            else:  # Render plain covered cell
                self._set_image(Cell.cover_img)

    def enable_debug(self):
        """
        Render debug coordinates over unrevealed cell. NOTE: This is a one-time
        state set; cannot disable once enabled during lifetime of the cell.
        """
        self.show_debug = True

    def get_values(self) -> tuple:
        """
        Get the representative values for the cell.
        Returns:
        revealed - 1 if revealed, otherwise 0.
        touching - Number of touching cells (-1 if not revealed).
        """
        if self.revealed:
            if not self.bomb:
                return 1, self.touching
            else:
                return 1, -1
        else:
            return 0, -1

    @staticmethod
    def value_to_rgba(val: int) -> tuple:
        """
        Convert cell value to RGBA value. Can support
        up to value 15, albeit up to value 8 is only
        useful.
        Arguments:
        val - Cell value.
        Returns:
        RGB tuple.
        """
        if val <= 0 or val > 15:
            return (90, 90, 90)  # Gray unrevealed
        elif val <= 7:
            cset = [0 for _ in range(3)]
            power = len(cset) - 1
            remainder = val
            for power in range(len(cset) - 1, -1, -1):
                bin_val = 2 ** power  # Binary value if current val is 1
                if bin_val <= remainder:
                    v = 255  # Max out the current value
                    cset[power] = v
                    remainder -= bin_val
                if remainder <= 0:
                    break
            return cset
        else:  # Special case for >= 8
            if val >= 8:  # Probably unecessary check
                return (255, 100, 0)  # Orangey color

    def get_summary(self):
        """
        Get a brief summary about the cell.
        Returns:
        Summary string.
        """
        return "Cell {}: bomb={}, revealed={}, touching={}, flagged={}".format(
            (self.i, self.j),
            self.bomb,
            self.revealed,
            self.touching,
            self.flagged)

    def _set_image(self, im):
        """
        Set the current image by copy.
        Arguments:
        im - Image surface.
        """
        self.image = copy.copy(im)

    def action(self, cb=None):
        """
        Draw over the current image for the cell with the new information.
        Arguments:
        cb - Callback if valid click is made. Only argument is cell itself.
        """
        if not self.actDebounce and not self.flagged:
            self.actDebounce = True
            self.showSurrounding(cb)  # Only if touching = 0
            # print(self.get_summary())
            if cb is not None and not self.revealed:
                cb(self)
            self.revealed = True

    def flag(self):
        """
        Add the flag image over the cell if it is flagged.
        Remove flag image from the cell if it is being un-flagged.
        """
        self.flagged = not self.flagged

    def showSurrounding(self, cb=None):
        """
        For all of the surrounding cells, reveal.
        Only called when the self.touching == 0.
        Arguments:
        cb - Callback that action() recieves.
        """
        if self.touching == 0 and not self.bomb:
            for neighbor in self.surrounding:
                neighbor.action(cb)

    def coordinates(self):
        """
        Get a tuple of the grid coordinates of this cell.
        Returns:
        Tuple coordinates (i, j).
        """
        return (self.i, self.j)