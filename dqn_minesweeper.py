"""DQN Agent for minesweeper.
"""
from keras.models import Model
from keras.layers import Dense, Input, Flatten, Conv2D, MaxPooling2D, Reshape
from keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
import gym

import apcspminesweeper  # NOQA

ENV_NAME = "apcsp-minesweeper-v0"


class DQNMinesweeperPlayer:

    def __init__(self):
        self.env = gym.make(ENV_NAME)

        nb_actions = self.env.action_space.n
        # self.model.add(Input((self.env.rows, self.env.cols, 3)))
        inp = Input(shape=(1,) + self.env.observation_space.shape)
        flat0 = Reshape((450, 450, 3))(inp)
        conv1 = Conv2D(32, 2,
                       activation="relu",
                       data_format="channels_last")(flat0)
        pool1 = MaxPooling2D(strides=(2, 2))(conv1)
        conv2 = Conv2D(32, 2, activation="relu")(pool1)
        pool2 = MaxPooling2D()(conv2)
        conv3 = Conv2D(32, 2, activation="relu")(pool2)
        flat = Flatten()(conv3)
        hidden1 = Dense(32)(flat)
        out = Dense(nb_actions, activation="linear")(hidden1)
        self.model = Model(inputs=inp, outputs=out)
        print(self.model.summary())

        self.mem = SequentialMemory(limit=50000, window_length=1)
        self.policy = BoltzmannQPolicy()
        self.agent = DQNAgent(model=self.model,
                              nb_actions=nb_actions,
                              memory=self.mem,
                              nb_steps_warmup=10,
                              target_model_update=1e-2,
                              policy=self.policy)
        self.agent.compile(Adam(lr=1e-3), metrics=["mae"])
        self.agent.fit(self.env, nb_steps=500000, visualize=True, verbose=2)
        self.agent.save_weights("dqn_{}_weights.h5".format(ENV_NAME),
                                overwrite=True)
        self.agent.test(nb_episodes=5, visualize=True)


if __name__ == "__main__":
    DQNMinesweeperPlayer()
