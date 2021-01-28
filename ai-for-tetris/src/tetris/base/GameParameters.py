class GameParameters:
    """
        Data class holding all game parameters

        Supported parameters are :
            board_size: two int tuple
                The size of the board
            pieces: array of src.tetris.base.Piece
                The pieces for the game to use
            seed: int
                The seed for the random number generator
            line_score: int
                Score acquired for completing a single line in the first level
            initial_speed: int
                The speed at the beginning of the game
            speed_update_policy: function
                Function returning the new speed when hitting next level. The
                function takes as argument the current speed (int) and return
                another int.
            line_scoring_policy: function
                Function returning the score when completing a given amount of
                lines at a given level. The function takes as a first argument
                the number of line removed (int), as a second argument the
                current level of the game (int) and returns the corresponding
                score (int)
            piece_scoring_policy: function
                Function returning the score when placing a piece on the board.
                The function takes as a first argument the position at which the
                piece was placed (tuple of two int), as a second argument the
                current level of the game (int) and returns the corresponding
                score (int)
    """

    def __init__(self, **kwargs):
        """
            Ctor

            Parameters
            ----------
                kwargs: non-positional arguments
                    board_size: two int tuple
                        The size of the board
                    pieces: array of src.tetris.base.Piece
                        The pieces for the game to use
                    seed: int
                        The seed for the random number generator
                    line_score: int
                        Score acquired for completing a single line in the
                        first level
                    initial_speed: int
                        The speed at the beginning of the game
                    speed_update_policy: function
                        Function returning the new speed when hitting next
                        level. The function takes as argument the current
                        speed (int) and return another int.
                    line_scoring_policy: function
                        Function returning the score when completing a given
                        amount of lines at a given level. The function takes as
                        a first argument the number of line removed (int), as a
                        second argument the current level of the game (int) and
                        returns the corresponding score (int)
                    piece_scoring_policy: function
                        Function returning the score when placing a piece on the
                        board. The function takes as a first argument the
                        position at which the piece was placed (tuple of
                        two int), as a second argument the current level of the
                        game (int) and returns the corresponding score (int)
        """
        self.board_size = kwargs.get("board_size", (20, 10))
        self.pieces = kwargs.get("pieces", [])
        self.seed = kwargs.get("seed", None)
        self.line_score = kwargs.get("line_score", 50)
        self.initial_speed = kwargs.get("initial_speed", 35)
        self.speed_update_policy = kwargs.get(
            "speed_update_policy", lambda speed: speed
        )
        self.line_scoring_policy = kwargs.get(
            "line_scoring", lambda ln, ll: self.line_score * ln ** 2 * (1 + ll)
        )
        self.piece_scoring_policy = kwargs.get(
            "piece_scoring_policy", lambda pos, lvl: (pos[0] + lvl + 1) ** 2
        )
        self.next_level_policy = kwargs.get(
            "next_level_policy", lambda lvl, lns: lns % 40 == 0 and lns != 0
        )
