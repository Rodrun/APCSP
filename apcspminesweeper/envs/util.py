"""Utility functions.
"""
from pygame.image import load
from pygame.transform import scale
from pygame import Rect


def load_scaled(path, dim: set):
    """
    Load an image and scale.

    Arguments:
    path - Path to image.
    dim - Dimensions of image.
    """
    return scale(load(path), dim)


def pt_within(p: set, r: Rect) -> bool:
    """
    Check if point p is within rectangle r.
    Arguments:
    p - Point to check.
    r - Rectangle object.
    Returns:
    True if point within rectangle, False otherwise.
    """
    return r.collidepoint(p)
