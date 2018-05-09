"""Grid cell object.
"""
import copy

import pygame


class Cell(pygame.sprite.Sprite):

    bomb_img = None  # Bomb image
    cover_img = None  # Unclicked image
    uncover_img = None  # Revealed image
    font = None  # Font to display # touching bombs

    def __init__(self, x, y, w, rows=9, cols=9):
        """
        Arguments:
        bomb - Is bomb?
        x - X coordinate.
        y - Y coordinate.
        w - Width of cell.
        rows - Rows of parent grid.
        cols - Columns of parent grid.
        """
        super().__init__()
        self.i = x
        self.j = y
        self.x = x * w
        self.y = y * w
        self.w = w
        self._set_image(Cell.cover_img)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.bomb = False
        self.revealed = False
        self.flagged = False
        self.touching = 0
        self.rows = rows
        self.cols = cols
        self.actDebounce = False
        self.surrounding = []
        self.tagged = False
        self.rendered_text = False  # To prevent Font.render() multiple times

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
        else:
            self._set_image(Cell.cover_img)

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

    def action(self):
        """
        Draw over the current image for the cell with the new information.
        """
        if not self.actDebounce and not self.flagged:
            self.actDebounce = True
            self.color = (90, 90, 90)
            self.revealed = True
            self.showSurrounding()  # Only if touching = 0
            # print(self.get_summary())

    def flag(self):
        """
        Add the flag image over the cell if it is flagged.
        Remove flag image from the cell if it is being un-flagged.
        """
        self.flagged = not self.flagged

    def showSurrounding(self):
        """
        For all of the surrounding cells, reveal.
        Only called when the self.touching == 0.
        """
        if self.touching == 0 and not self.bomb:
            for neighbor in self.surrounding:
                neighbor.action()
