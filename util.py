"""Utility functions.
"""
from pygame.image import load
from pygame.transform import scale


def load_scaled(path, dim: set):
    """
    Load an image and scale.

    Arguments:
    path - Path to image.
    dim - Dimensions of image.
    """
    return scale(load(path), dim)
