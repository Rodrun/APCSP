"""Game UI container that is seen above the grid.
"""
import pygame


class UIContainer(pygame.sprite.LayeredUpdates):

    def __init__(self, height, dfont="digital-7.ttf", font_ratio=.4):
        """
        Arguments:
        dfont - Font to use.
        """
        assert dfont is not None
        self.font = pygame.font.Font(dfont,
                                     int(height * font_ratio))
