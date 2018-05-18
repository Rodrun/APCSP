"""Minesweeper grid environment space.
"""
import gym

from grid import Grid


class GridSpace(gym.Space):

    def __init__(self, origin: Grid):
        """
        Arguments:
        origin - Original grid object to represent.
        """
        self.origin = origin

    def contains(self, x):
        pass

    def sample(self):
        pass
