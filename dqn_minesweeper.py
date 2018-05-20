"""DQN Agent for minesweeper.
"""
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.policy import BlotzmannQPolicy
from rl.memory import SequentialMemory
import gym

ENV_NAME = "apcsp-minesweeper"


class DQNMinesweeperPlayer:

    def __init__(self):
        self.env = gym.make(ENV_NAME)
        self.model = Sequential()
        self.model.add(Flatten(input_shape=(1,)
                       + self.env.observation_space.shape))
        self.model.add(Dense(81))
        self.model.add(Activation("relu"))
        self.model.add(Dense(81))
        self.model.add(Activation("relu"))
        self.model.add(Dense(self.env.action_space.n))
        print(self.model.summary())
        self.mem = SequentialMemory(limit=50000, window_length=1)
        self.policy = BlotzmannQPolicy()
        self.agent = DQNAgent(model=self.model,
                              nb_actions=self.env.action_space.n,
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
