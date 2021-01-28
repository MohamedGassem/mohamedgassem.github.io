import numpy as np
import copy

from src.tetris.base.Controls import Controls
from src.tetris.base.TetrisBase import TetrisBase
from src.tetris.base.GameParameters import GameParameters

from src.AI.metrics import *

class QLearningAI:
    """
        QLearning implementation for tetris 

        See QLearning wikipedia page for more detail on the algorithm

        As the board is filled with 0 and 1, each state can be represented
        as an unique integer, the board giving its binary representation.

        Warning : the QTable is kept in memory. Thus if the board is too large
        the QTable might not feed. A different implementation using file storage
        instead of RAM must then be considered.
    """

    def __init__(self, game_params, learning_rate = 0.02, 
                       discount_factor = 0.8, seed = None):
        """
            Ctor

            Parameters
            ----------
                game_params: src.tetris.base.GameParameters
                    The parameters for the game the AI must train on
                learning_rate: float 
                    The learning rate of the model
                discount_factor: float
                    The discount factor of the model
                seed: int
                    The random initializer seed
        """
        self._gameparams = game_params
        self._random = np.random.RandomState(seed)

        self._ctrls = list(Controls)
        self._ctrls.remove(Controls.STORE)

        self._power_of_two = 2 ** np.arange(np.prod(game_params.board_size))
        actions = len(self._ctrls)

        self._qtable = np.zeros(
            shape = (self._power_of_two[-1] * 2, actions)
        )
        self._lr = learning_rate
        self._df = discount_factor

    def _board_to_state(self, board):
        """
            Compute decimal representation of the board (big endianness)

            Parameters
            ----------
                board: 2d array like of 0 or 1
                    The current state of the board
            
            Returns
            -------
                int
                    The integer representation of the board 
        """
        flt = board.flatten()
        return sum(self._power_of_two[flt == 1])

    def save(self, filename):
        """
            Saves the qtable to a file

            Parameters
            ----------
                filemane: str
                    The path to the file to save the QTable into
        """
        np.save(filename, self._qtable)
    
    def load(self, filename):
        """
            Loads the QTable from a file

            Parameters
            ----------
                filemnae: str
                    The path to the file where the QTable must be loaded from
        """
        self._qtable = np.load(filename)

    def _reward(self, board, new_board, 
                      score, new_score, 
                      lines, new_lines):
        if lines != new_lines:
            return 10000

        a = compute_sum_height(new_board)
        c = new_lines - lines
        h = compute_holes(new_board)
        b = compute_bumpiness(new_board)

        return -0.5 * a + 0.7 * c - 0.35 * h - 0.18 * b

    def train_for(self, game_count, max_it = 1000000):
        """
            Trains the model for a given amount of game

            Parameters
            ----------
                game_count: int
                    The number of game to be played
                max_it: int
                    An upper bound for the total number (not reseted after the
                    end of a game) of turn the AI can play. This number 
                    garentees the function will exit even if the AI is playing 
                    perfectly. 
        """
        # print(self._qtable)
        game_index = 0
        it_index = 0

        try:
            while (game_index < game_count) and (it_index < max_it):
                tetris = TetrisBase(self._gameparams)

                while not tetris._is_over:
                    statesactions = []
                
                    start_board = copy.deepcopy(tetris._board[:-1, 1:-1])
                    start_score = tetris._score
                    start_lines = tetris._lines_count

                    new_board = []
                    new_score = tetris._score
                    new_lines = tetris._lines_count

                    reward = 0
                    # While a piece hasn't been placed
                    while new_score == start_score:
                        # Current information
                        board = tetris.get_current_game_state()
                        board = board[:-1, 1:-1]
                        state = self._board_to_state(board)

                        line_count = tetris._lines_count
                        
                        # Get the action then perform it
                        if np.random.uniform(0, 1) < 0.1:
                            action = np.random.choice(range(0, len(self._ctrls)))
                        else:
                            action = np.argmax(self._qtable[state])
                        
                        tetris.tick(self._ctrls[action])
                        
                        # New state
                        new_board = tetris.get_current_game_state()
                        new_board = new_board[:-1, 1:-1]
                        new_state = self._board_to_state(new_board)

                        # Number of line cleared
                        new_score = tetris._score
                        new_lines = tetris._lines_count

                        statesactions.append({
                            "state": state, 
                            "action": action, 
                            "new_state": new_state
                        })

                    reward = self._reward(start_board, tetris._board[:-1, 1:-1], 
                                          start_score, new_score,
                                          start_lines, new_lines)

                    visited = []
                    rwdfactor = 1

                    for stateaction in statesactions[::-1]:
                        state  = stateaction["state"]
                    
                        if not (state in visited):
                            visited.append(state)

                            action = stateaction["action"]
                            new_state = stateaction["new_state"]

                            rwd = rwdfactor * reward
                            rwdfactor *= 0.75

                            optimal = np.max(self._qtable[new_state])

                            self._qtable[state, action] = (
                                    (1 - self._lr) * self._qtable[state, action] + 
                                         self._lr  * (rwd + self._df * optimal))  

                    it_index = it_index + 1            
                game_index = game_index + 1
                print("Game ", game_index, " is over, score : ", tetris._score)   
        except KeyboardInterrupt:
            pass

    def predict(self, board):
        board = board[:-1, 1:-1]
        state = self._board_to_state(board)
        
        action = np.argmax(self._qtable[state])
        
        #print("Board : ")
        #print(board)
        #print(self._qtable[state])
        print(self._ctrls[action])


        return self._ctrls[action]
