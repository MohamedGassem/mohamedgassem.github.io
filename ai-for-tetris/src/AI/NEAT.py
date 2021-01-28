import numpy as np
import copy

import neat
import pickle

from src.AI.metrics import *

from src.AI.visualize import draw_net
from src.AI.visualize import plot_stats
from src.AI.visualize import plot_species

from src.tetris.base.Controls import Controls
from src.tetris.base.TetrisBase import TetrisBase
from src.tetris.base.GameParameters import GameParameters

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))

class NEATAI:
    """
        Neat AI playing python
    """

    def __init__(self, config_path, gameparams):
        """
            Ctor

            Parameters
            ----------
                config_path: string
                    Path to neat-python config file
                gameparams: src.tetris.base.GameParameters
                    The parameters for the games to train on
        """
        self._config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)

        self._params = gameparams
        self._ctrls = list(Controls)
        self._ctrls.remove(Controls.STORE)

    def _reward(self, start_board, start_lines, start_score, 
                        new_board,   new_lines,   new_score):
        """
            Compute the reward between two tetris states

            Parameters
            ----------
                start_board: 2d array_like
                    The previous board 
                start_line: int
                    The previous number of cleared lines
                start_score: int
                    The previous score 
                new_board: 2d array_like
                    The new board 
                new_line: int
                    The new number of cleared lines
                new_score: int
                    The new score 
        """
        if start_lines != new_lines:
            return 0
            
        return max(0, bumpiness(new_board) - bumpiness(start_board))

    def train(self, generation = 10):   
        """
            Trains the AI for a given number of generation

            During the training, the fitness of each genome is printed and a 
            summary of the generation is done.
            At the end of training, a graphical summary of all generation is
            given. The training process does not save anything ! 

            Note that most of the parameters are located in the config
            file

            Parameters
            ----------
                generation: int
                    The number of generation to train the AI on
        """     
        p = neat.Population(self._config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.eval_genomes, generation)
        print('\nBest genome:\n{!s}'.format(winner))

        #draw_net(self._config, winner, True)
        plot_stats(stats, ylog=False, view=True)
        plot_species(stats, view=True)

        self._winning_genome = winner
        self._nn = neat.nn.FeedForwardNetwork.create(winner, self._config)

    
    def eval_genomes(self, genomes, config):
        """
            Evaluates the fiteness of a set of genomes

            Parameters
            ----------
                genomes: list of (int, neat genome)
                    The genomes to evaluate the fitness of
                config: neat config 
                    The configuration
        """

        # Prevent AI to play indefinitly
        max_action_per_game = 100000

        for genome_id, genome in genomes:
            genome.fitness = 0.0

            # Create neural network
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            tetris = TetrisBase(self._params)
            
            pieces_count = 0
            action_count  = 0

            # Play the game
            while not tetris._is_over:
                # Save initial state of the board
                start_board = copy.deepcopy(tetris._board[:-1, 1:-1])
                start_lines = tetris._lines_count

                score = tetris._score
                new_score = score

                # While the current piece is not placed
                while score == new_score:
                    board = tetris.get_current_game_state()
                    board = board[:-1, 1:-1]
                    board = board.flatten()

                    # Play the "best" move
                    out = net.activate(board)
                    # Softmax to obtain a probability vector
                    out = softmax(out)

                    action = np.argmax(out)
                    mvt = self._ctrls[action]

                    tetris.tick(mvt)

                    new_score = tetris._score
                    action_count = action_count + 1
                    
                    # Stop the AI when reaching the max action
                    if action_count > max_action_per_game:
                        print("Reach action count limit")
                        tetris._end()
                        break

                new_board = tetris._board[:-1, 1:-1]
                a = compute_sum_height(new_board)
                c = tetris._lines_count - start_lines
                h = compute_holes(new_board)
                b = compute_bumpiness(new_board)

                metric =  -0.5 * a + 0.7 * c - 0.35 * h - 0.18 * b
                genome.fitness += metric

            # Evaluate fitness
            genome.fitness  = metric / action_count
            print("Genore : ", genome_id, ", fitness : ", genome.fitness)
        
    def save(self, file):
        """
            Saves the current AI to a file

            Parameters
            ----------
                file: string
                    The path to the file where the AI needs to be saved into
        """
        with open(file, "wb") as save_file:
            pickle.dump(self._winning_genome, save_file)
            save_file.close()

    def load(self, file):
        """
            Loads an AI from a file

            Parameters
            ----------
                file: string
                    The path to the file where the AI needs to be loaded from
        """
        with open(file, "rb") as load_file:
            self._winning_genome = pickle.load(load_file)
            self._nn = neat.nn.FeedForwardNetwork.create(
                self._winning_genome, self._config)
    
    def predict(self, board, print_raw = True):
        """
            Makes a prediction given the board

            Note: the board must include boundaries

            Parameters
            ----------
                board: 2d array_like
                    The board to predict from
                print_raw: bool
                    If true, prints the probability vector
            
            Returns
            -------
                src.tetris.base.Controls
                    The controls to perform
        """
        board = board[:-1, 1:-1]
        board = board.flatten()

        out = self._nn.activate(board)
        out = softmax(out)

        action = np.argmax(out)
        mvt = self._ctrls[action]

        if print_raw:
            print("=================================")
            probas = {self._ctrls[i]: out[i] for i in range(0, len(self._ctrls))}
            
            for m, p in probas.items():
                if m == mvt:
                    print(" ** ", m, ": ", p)
                else:
                    print("    ", m, ": ", p)
            print("=================================")
        return mvt