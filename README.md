# Minesweeper with AI

-Train a neural network model to play minesweeper using reinforcement learning.
-Create an algorithm that can play the minesweeper game using logic.

For APCSP final project.

## Development setup
1. Start virtual environment: `pipenv shell`
2. Install deps: `pipenv install -e .`
3. Install the gym environment: `python setup.py`


## Normal Minesweeper game
Run `minesweeper.py` _from_ the root directory.

i.e. `python apcspminesweeper/envs/minesweeper.py`

See the top docstring for extra controls and information.


## Dependencies

All dependencies by `pipenv`, but this project heavily relies on:

- [pygame](https://pygame.org)
- [keras-rl](http://keras-rl.readthedocs.io/en/latest/)
- [openai-gym](https://gym.openai.com/)
