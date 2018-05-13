"""AI that learns to play minesweeper.
"""
import math

import neat

from minesweeper import Minesweeper


class AI:

    def __init__(self, mine, config_file="ai/config"):
        """
        Initialize the GANN.
        Arguments:
        mine - Minesweeper instance.
        config_file - NEAT Configuration file.
        """
        self.config = neat.Config(neat.DefaultGenome,
                                  neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet,
                                  neat.DefaultStagnation,
                                  config_file)
        self.config.genome_config.add_activation("ms_sigmoid",
                                                 AI.ms_sigmoid)
        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)
        self.population.add_reporter(neat.Checkpointer(1))

        self.game = mine
        self.curr_remaining = None
        self.curr_fitness = 0.0
        self.game.set_end_callbacks([self._end_call])
        self.game.set_click_callbacks([self._after_click])

    def _after_click(self, cell, remaining):
        """
        Callback after a cell click.
        """
        self.curr_remaining = remaining

    def _end_call(self, remaining, lost):
        self.playing = False  # Breaks the loop when evaluating genome
        self.curr_fitness = AI.get_fitness(remaining,
                                           self.game.get_total_cells()
                                           - self.game.bomb_limit)

    @staticmethod
    def get_fitness(remaining, max):
        """
        Calculate fitness.
        Arguments:
        remaining - Remaining amount of non-bomb cells.
        max - Maximum amount of cells that are not bombs.
        Returns:
        Fitness.
        """
        return max - remaining

    def run(self, generations=300):
        """
        Run the genetic algorithm.
        Arguments:
        generations - Maximum amount of generations to run.
        Returns:
        First winning genome (fitness = 1.0).
        """
        return self.population.run(self.evaluate, generations)

    def evaluate(self, genomes, config):
        """
        Genome evaluation function.
        """
        quit_requested = False  # If game.update() is False
        for genome_id, genome in genomes:
            # Setup
            self.game.reset()
            self.playing = True
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            while self.playing:
                # Get current grid values
                curr_grid = [v for v in self.game.get_grid_vals()]
                # print(len(curr_grid), ":", curr_grid)
                # Get click coordinate prediction
                output = net.activate(curr_grid)
                x = int(round(output[0]))
                y = int(round(output[1]))
                # Click on prediction
                if not self.game.grid.at(x, y).revealed:
                    print("VALID prediction: ", output)
                    self.game.click_cell(x, y)
                else:
                    print("INVALID prediction: ", output)
                    # self.game.end_game(True)

                quit_requested = not self.game.update()
                if quit_requested:
                    break
                self.game.draw()

            # curr_fitness is set after playing loop is broken
            genome.fitness = self.curr_fitness

            if quit_requested:
                assert False, "quit requested"

    @staticmethod
    def ms_sigmoid(x):
        if x == -1:
            return 1 / (1 + math.pow(math.e, -x))
        else:
            return 0


if __name__ == "__main__":
    parser = Minesweeper.arg_parser()
    parser.add_argument("--generations",
                        type=int,
                        default=300,
                        help="max amount of generations to run")
    args = parser.parse_args()
    minesweeper = Minesweeper.from_args(parser)
    minesweeper.user_input = False
    ai = AI(minesweeper)
    winner = ai.run(generations=args.generations)
    # print("WINNER: ", winner)
