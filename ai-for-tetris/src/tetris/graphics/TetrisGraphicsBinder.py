from src.tetris.base.Controls import Controls
from src.tetris.graphics.TetrisGraphics import TetrisGraphics

class TetrisGraphicsBinder(TetrisGraphics):
    """
        Binds an external player (or set of command) to 
        the tetris graphics class
    """

    def __init__(self, player, graphical_params, game_params):
        """
            Ctor

            Parameters
            ----------
                player: function
                    A function that takes the current board as parameters and 
                    returns the corresponding action (Controls) to perform
                graphical_params: GraphicalParametersEu
                    The display parameters for the game. See
                    src.tetris.graphics.GraphicalParameters for more information
                    about those parameters.
                game_params: GameParameters
                    Parameters for the game. See class documentation for more
                    details
        """
        super().__init__(graphical_params, game_params)
        self._player = player
        self._mvt = []

    def on_update(self, events = ""):
        """
            Overrides on_update method, ignoring second parameter

            Parameters
            ----------
                events: any
                    Not used, just here for the sake of compatibility 
                    with main class
        """
        if len(self._mvt) == 0:
            mvts = self._player(self.get_current_game_state())

            if type(mvts) is Controls:
                self._mvt = [mvts]
            else:
                self._mvt = mvts

        if len(self._mvt) != 0:
            #print(self._mvt[0])
            mvt = self._mvt.pop(0)
            #input("\n")
        else:
            mvt = Controls.NOTHING

        self.tick(mvt)
