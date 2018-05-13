"""AI that learns to play minesweeper.
"""
import neat

from minesweeper import Minesweeper


class AI:

    def __init__(self, mine, config_file="ai/config"):
        self.config = neat.Config(neat.DefaultGenome,
                                  neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet,
                                  neat.DefaultStagnation,
                                  config_file)
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
        self.curr_fitness = AI.get_fitness(remaining,
                                           self.game.get_total_cells())

    @staticmethod
    def get_fitness(remaining, max):
        """
        Calculate fitness.
        Arguments:
        remaining - Remaining amount of cells.
        max - Maximum amount of cells.
        Returns:
        Fitness.
        """
        return remaining

    def evaluate(self, genomes, config):
        """
        Evaluate genomes.
        """
        for genome_id, genome in genomes:
            genome.fitness = 1.0
            playing = True
            while playing:
                pass
            # Evaluate fitness
            genome.fitness = 0.0


if __name__ == "__main__":
    parser = Minesweeper.arg_parser()
    minesweeper = Minesweeper.from_args(parser)
