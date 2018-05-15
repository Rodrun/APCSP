"""Dead.
"""
import math

import neat

from minesweeper import Minesweeper

"""AI that learns and plays minesweeper.
"""


if __name__ == "__main__":
    parser = Minesweeper.arg_parser()
    args = parser.parse_args()
    minesweeper = Minesweeper.from_args(parser)
    minesweeper.user_input = False
