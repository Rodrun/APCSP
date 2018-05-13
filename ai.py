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
        self.curr_grid = None
        self.curr_fitness = 0.0

    def _end_call(self, grid):
        pass

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
