"""Teach the model to play.
"""
import os

import numpy as np
from keras.layers import Conv2D
from keras.models import Sequential, load_model

from minesweeper import Minesweeper


class AILearn:

    # Save configuration
    MODEL_NAME = "msweeper-ai"  # h5 extension not included
    MODEL_DIR = "ai"
    # Combines MODEL_NAME + MODEL_DIR
    MODEL_PATH = os.path.join(os.getcwd(), MODEL_DIR)

    def __init__(self, game: Minesweeper, model_path: str = None):
        """
        Arguments:
        game - Minesweeper game.
        model_path - Path to model. None creates a new one.
        """
        # Setup
        if not os.path.isdir(AILearn.MODEL_DIR):
            os.mkdir(AILearn.MODEL_DIR)

        self.game = game
        assert game is not None

        # Model load
        self.model_path = model_path
        if model_path is None:  # New model
            self.model = Sequential()
            # Theano uses channel first
            input_shape = (2, game.rows, game.cols)
            self.model.add(Conv2D(3,
                                  input_shape=input_shape))
        else:
            self.model = load_model(model_path)

    def save(self, path: str = None):
        """
        Save the current model.
        Arguments:
        path - Path to save to. If None, will save to MODEL_DIR/MODEL_NAME.h5.
        """
        if path is not None:
            self.model.save(path)
        else:
            self.model.save(os.path.join(AILearn.MODEL_DIR,
                                         AILearn.MODEL_NAME + ".h5"))
