
import numpy as np
from src.tetris.base.Controls import Controls


class RandomAI:
    """
        "AI" that plays tetris with random moves

        This "AI" has no interest has such but allows
        to see that other may have learn at least one thing
    """

    def __init__(self, seed = None):
        """
            Ctor

            Parameters
            ----------
                seed: int or None
                    The seed of the random number generator to use
        """
        self._random = np.random.RandomState(seed)

        self._ctrls = list(Controls)
        # Remove unsuported option
        self._ctrls.remove(Controls.STORE)

    def predict(self, board):
        """
            Makes a "prediction" given the current board

            In fact, the board isn't used and the AI plays
            randomly

            Parameters
            ----------
                board: anythin
                    Unused parameter but supposed to represent
                    the current tetris board
        """
        return self._random.choice(self._ctrls)