"""Game UI container that is seen above the grid.
"""
import pygame


class UIContainer(pygame.sprite.LayeredUpdates):

    def __init__(self, dfont=""):
        """
        Arguments:
        dfont - Font to use.
        """
        self.dfont = dfont
        if dfont is None:
            # Use default font
            pass
