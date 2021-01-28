import itertools
import numpy as np
import copy
import time
import pprint

from src.AI.metrics import *

from src.tetris.base.Controls import Controls
from src.tetris.base.TetrisBase import TetrisBase
from src.tetris.base.GameParameters import GameParameters

from src.AI.GeneticAlgorithm import GeneticAlgorithm
from src.AI.GeneticAlgorithm import GeneticAlgorithmParameters
from src.AI.GeneticAlgorithm import GeneticAlgorithmStatistics 

def best_of_if(first, second):
    """
        Tells which move is the best

        Parameters
        ----------
            first: dictionnary
                The following required (string) keys are :
                    cleared: number of line cleared by the move
                    holes:   number of holes of the resulting board
                    bumpiness: bumpiness score of the resulting board
                    height: maximum height of the resulting board
                    aheight: sum of all column heights of the resulting board 
            second: dictionnary
                The following required (string) keys are :
                    cleared: number of line cleared by the move
                    holes:   number of holes of the resulting board
                    bumpiness: bumpiness score of the resulting board
                    height: maximum height of the resulting board
                    aheight: sum of all column heights of the resulting board
        
        Returns
        -------
            dict
                Either first or second
    """
    # Greater number of line cleared
    if first["cleared"] >= 3:
        if first["cleared"] > second["cleared"]:
            return first
        elif first["cleared"] < second["cleared"]:
            return second

    if first["holes"] > second["holes"]:
        return second
    elif first["holes"] < second["holes"]:
        return first
    else:
        if first["bumpiness"] > second["bumpiness"]:
            return second
        elif first["bumpiness"] < second["bumpiness"]:
            return first
        else:
            if first["aheight"] > second["aheight"]:
                return second                                                                                          
            elif first["aheight"] < second["aheight"]:   
                return second
            else:
                if first["lines"] > second["lines"]:
                    return first
                elif first["lines"] < second["lines"]:
                    return second
                else:
                        if first["score"] > second["score"]:
                            return first
                        return second

class LookupAI:
    """
        AI that tries the best move possible among all others

        Here, a move meets the following requirements : 
            It only changes position or orientation in the first row (meaning 
            that putting one piece below another is not possible)

        And best means : for a given metric, ignoring the upcomming piece
    """

    def __init__(self, gameparams, geneticparams):
        """
            Ctor

            Parameters
            ----------
                gameparams: src.tetris.base.GameParameters
                    The parameters used for the game. 
        """

        # Compute all moves possibles
        self._gameparams    = gameparams
        self._rotations = [
            [], 
            [Controls.ROTATE_LEFT], 
            [Controls.ROTATE_RIGHT], 
            [Controls.ROTATE_LEFT, 
            Controls.ROTATE_LEFT]
        ]

        self._tetris = None
        self._combination = []

        for ctrl in self._rotations:
            self._combination.append(ctrl)
            moves_left  = []
            moves_right = []

            for c in ctrl:
                moves_left.append(c)
                moves_right.append(c)

            for i in range(0, int(gameparams.board_size[0] / 2)):
                moves_left.append(Controls.LEFT)
                moves_right.append(Controls.RIGHT)

                self._combination.append(copy.deepcopy(moves_left))
                self._combination.append(copy.deepcopy(moves_right))

        # Setup algorithm
        self._game_count = 100
        self._max_pieces = 100
        self._coeffs = [0, 0, 0, 0]

        self._geneticparams = geneticparams
        self._geneticparams.genes_count = len(self._coeffs)
        self._geneticparams.fitness = self._fitness
        self._geneticalgorithm = GeneticAlgorithm(self._geneticparams)

    def _fitness(self, id, genome):
        print("Computing fitness for genome no : ", id)
        print("Current genome : ", genome)

        self._coeffs = genome 
        line_count = 0

        for i in range(0, self._game_count):
            print("Game ", i, "/", self._game_count)
            tetris = TetrisBase(self._gameparams)
            self.bind(tetris)

            piece_count = 0
            while (not tetris._is_over) and piece_count < self._max_pieces:
                moves = self.predict(None)

                for m in moves:
                    tetris.tick(m)
                
                piece_count += 1
            
            line_count += tetris._lines_count

        return line_count / self._game_count

    def _best_of(self, first, second):
        first_score = self._coeffs[0] * first["aheight"] + \
                      self._coeffs[1] * first["cleared"] + \
                      self._coeffs[2] * first["holes"]   + \
                      self._coeffs[3] * first["bumpiness"]
        
        second_score = self._coeffs[0] * second["aheight"] + \
                       self._coeffs[1] * second["cleared"] + \
                       self._coeffs[2] * second["holes"]   + \
                       self._coeffs[3] * second["bumpiness"]
        
        if first_score > second_score:
            return first
        
        return second

    def bind(self, tetris):
        """
            Binds a game to the AI
        """
        self._tetris = tetris
    
    def train(self, generations, game_count, piece_count):
        self._game_count = game_count
        self._max_pieces = piece_count
        
        stats = self._geneticalgorithm.train(generations)

        pp = pprint.PrettyPrinter(indent = 4)
        pp.pprint(stats)

    def predict(self, board):
        """
            Makes a prediction

            The bind function must be called before this function. Otherwise
            an EnvironmentError is raised

            Parameters
            ----------
                board: 2d array_like
                    Unused. Board infos are accessed through the bounded game
        """
        pp = pprint.PrettyPrinter(indent = 4)

        if self._tetris is None:
            raise EnvironmentError("Binds the AI to a game first")

        default = {
            "moves":        [],
            "lines":    -10000,
            "score":    -10000,
            "bumpiness": 10000,
            "holes":     10000,
            "height":    10000,
            "aheight":   10000,
            "cleared":  -10000 
        }

        best = copy.deepcopy(default)

        current_lines = self._tetris._lines_count
        ts = time.time()
        for moves in self._combination:
            m, board_, lines, score = self._tetris.try_moves(moves)
            
            holes      = compute_holes(board_)
            height     = compute_height(board_)
            bumpiness  = compute_bumpiness(board_)
            aggregated_height = compute_sum_height(board_)

            current = {
                "moves": m,
                "holes": holes, 
                "lines": lines, 
                "score": score, 
                "height": height,
                "aheight": aggregated_height,
                "cleared": lines - current_lines, 
                "bumpiness": bumpiness
            }

            if best == default:
                best = current
            else:
                best = self._best_of(best, current)
        
        #print("Computing best took : ", time.time() - ts)

        #print("=========== Best ================")
        #pp.pprint(best)

        return best["moves"]