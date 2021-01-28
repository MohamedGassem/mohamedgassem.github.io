import numpy as np
import pprint
from copy import copy, deepcopy



from src.tetris.base.Controls import Controls
from src.tetris.base.Piece import Piece


class TetrisBase:
    """
           Class that handles Tetris base game
    """

    def __init__(self, params):
        """
            Constructor

            Parameters
            ----------
                params: GameParameters
                    Parameters for the game. See class documentation for more
                    details
        """
        self._params = params
        # The class requires to maintain its own random state so multiple
        # instances can run in parallel with the "same randomness"
        self._random = np.random.RandomState(self._params.seed)

        self._current_speed = self._params.initial_speed
        self._current_time = 0

        self._board = self._create_empty_board()
        self._init_pieces()

        self._is_over = False

        self._level = 0
        self._score = 0
        self._lines_count = 0

    def tick(self, mvt=Controls.NOTHING):
        """
            Run a tick of the game

            Parameters
            ----------
                mvt: tetris.base.Controls.Controls
                    The action to perform on this tick
        """
        if self._is_over:
            return      

        self._handle_movement(mvt)
        self._current_time += 1

        if self._current_time >= self._current_speed:
            # Timer is always reset for down actions
            self._handle_movement(Controls.DOWN)
        
    def _handle_movement(self, mvt):
        """
            Inplace movement handling

            Parameters
            ----------
                mvt: tetris.base.Controls.Controls
                    The movement to process
        """
        if mvt is Controls.NOTHING:
            pass
        elif mvt is Controls.DOWN:
            bottom_pos = (self._current_pos[0], self._current_pos[1] + 1)

            if self._check_for_piece(bottom_pos, self._current_piece):
                self._current_pos = bottom_pos
            else:
                self._place_current_piece()
                lines = self._process_lines()
    
                self._lines_count += lines
                self._score += self._params.piece_scoring_policy(
                    self._current_pos, self._level
                )
                self._score += self._params.line_scoring_policy(
                    lines, self._level
                )

                next_level = self._params.next_level_policy(
                    self._level, self._lines_count
                )

                if next_level:
                    self._current_speed = self._params.speed_update_policy(
                        self._current_speed
                    )
                    self._level += 1

                self._draw_new_piece()

                is_end = not self._check_for_piece(
                    self._current_pos,
                    self._current_piece
                )

                if is_end:
                    self._end()

            # When pressing down reset timer to prevent 'double tap' effects
            self._current_time = 0
        elif mvt is Controls.LEFT:
            left_pos = (self._current_pos[0] - 1, self._current_pos[1])

            if self._check_for_piece(left_pos, self._current_piece):
                self._current_pos = left_pos
        elif mvt is Controls.RIGHT:
            right_pos = (self._current_pos[0] + 1, self._current_pos[1])

            if self._check_for_piece(right_pos, self._current_piece):
                self._current_pos = right_pos
        elif mvt is Controls.ROTATE_LEFT:
            rotate_piece = Piece(self._current_piece.rotate_left())
            rotate_pos = self._current_pos
            rotate_pos = self._compute_rotation_pos(rotate_pos, rotate_piece)

            if self._check_for_piece(rotate_pos, rotate_piece):
                self._current_piece.rotate_left(perform=True)
                self._current_pos = rotate_pos
        elif mvt is Controls.ROTATE_RIGHT:
            rotate_piece = Piece(self._current_piece.rotate_right())
            rotate_pos = self._current_pos
            rotate_pos = self._compute_rotation_pos(rotate_pos, rotate_piece)

            if self._check_for_piece(rotate_pos, rotate_piece):
                self._current_piece.rotate_right(perform=True)
                self._current_pos = rotate_pos
        elif mvt is Controls.STORE:
            # TODO : Implement piece storing
            pass
        else:
            raise NameError("Undefined control " + str(mvt))

    def _check_for_piece(self, pos, piece):
        """
            Check if a current position is valid for a piece

            A piece is considered in a valid spot iff the Hadamard Product
            (component wise multiplication) between the piece and the board
            is the null matrix meaning no two non null elements are in the
            same place.

            Parameters
            ----------
                pos: two int tuple
                    The position to check for
                piece: tetris.base.Piece
                    The piece to check for

            Returns
            -------
                bool
                    True if the piece is at a valid position, false otherwise
        """
        indices, piece_data = piece.compute_current_bounds()

        top = pos[1] + indices[0]
        left = pos[0] + indices[2]
        bottom = pos[1] + indices[1]
        right = pos[0] + indices[3]

        board_data = self._board[top:bottom + 1, left:right + 1]
        return np.count_nonzero(piece_data * board_data) == 0

    def _place_current_piece(self):
        """
            Place the current piece on the board
        """
        indices, piece_data = self._current_piece.compute_current_bounds()

        top = self._current_pos[1] + indices[0]
        left = self._current_pos[0] + indices[2]
        bottom = self._current_pos[1] + indices[1]
        right = self._current_pos[0] + indices[3]

        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                if piece_data[i - top][j - left] != 0:
                    self._board[i][j] = piece_data[i - top][j - left]

    def _process_lines(self):
        """
            Removes the completed lines

            Returns
            -------
                int
                    The number of line that were removed
        """
        size = self._params.board_size
        board = self._create_empty_board()

        line_count = 0

        current_offset = size[0] - 1
        for i in reversed(range(0, size[0])):
            # Check if the line is full
            if np.count_nonzero(self._board[i]) == size[1] + 2:
                # Increment line_count and ignore copying current line without
                # decrement current_offset to make the drop down effect
                line_count = line_count + 1
            else:
                # Line is not filled, copy current line then try copying the
                # above line
                board[current_offset] = self._board[i]
                current_offset = current_offset - 1

        self._board = board
        return line_count

    def _compute_rotation_pos(self, pos, rotated_piece):
        """
            Compute position for rotation

            When a rotation occurs, it is possible that position is invalidated,
            one example might be if the piece is in the boundary. This function
            compute the necessary left/right shifting for the piece not to be
            inside the boundary.

            Note : This function does not guarantee that the returned position
            is valid (ie it does not collide with previous pieces)

            Parameters
            ----------
                pos: tuple of two int
                    The current position of the piece (before rotation)
                rotated_piece: tetris.base.Piece
                    The rotated piece

            Returns
            -------
                Tuple of two int
                    A position where the rotated piece does not collide with
                    the boundary
        """
        size = self._params.board_size
        indices, _ = rotated_piece.compute_current_bounds()

        # Position may be negative so take into account boundary and eventual
        # shifting
        x_component = max(1, pos[0])
        x_component = min(x_component, size[1] - indices[3])

        return x_component, pos[1]

    def _create_empty_board(self):
        """
            Creates an empty board

            An empty board is defined as a matrix whose first and last column
            as well as the last row are filled with non null (1) elements
        """
        size = self._params.board_size
        board = np.zeros((size[0] + 1, size[1] + 2))

        board[:, size[1] + 1] = 1.0
        board[:, 0] = 1.0
        board[size[0], :] = 1.0

        return board

    def _init_pieces(self):
        """
            Sets current, next and stored pieces
        """
        # Current piece
        self._current_piece = None
        # Stored piece
        self._store_piece = None
        # The next piece;
        # the game must provide information about upcoming pieces
        self._next_piece = None

        # Position of the current piece
        self._current_pos = None

        # Create _next_piece, _current_piece is still None
        self._draw_new_piece()
        # _current_piece becomes _next_piece then draw another next piece
        self._draw_new_piece()

    def _draw_new_piece(self):
        """
            Draws a new piece

            This function first make the current piece become the provided next
            piece then (randomly) draw a new piece
        """
        size = self._params.board_size
        self._current_piece = self._next_piece

        random_piece = self._random.randint(0, len(self._params.pieces))
        # Deepcopy required since the list might be shared with other instances
        # and we do not want to alter its content
        self._next_piece = deepcopy(self._params.pieces[random_piece])

        # Sets position to be the middle of the game
        if self._current_piece is not None:
            current_shape = self._current_piece.get_current_state().shape
            center = int((size[1] - current_shape[1]) / 2)
            self._current_pos = (1 + center, 0)

    def get_current_game_state(self):
        """
            Returns the board with the current piece drawn inside

            Returns
            -------
                2D numpy array
                    The board with the current piece drawn inside
        """
        indices, piece_data = self._current_piece.compute_current_bounds()

        top = self._current_pos[1] + indices[0]
        left = self._current_pos[0] + indices[2]
        bottom = self._current_pos[1] + indices[1]
        right = self._current_pos[0] + indices[3]

        boards = deepcopy(self._board)
        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                if piece_data[i - top][j - left] != 0:
                    boards[i][j] = piece_data[i - top][j - left]

        return boards

    def _restart(self):
        """
            Restarts the game

            The restart is effective even if the game is not over yet
        """
        self._is_over = False
        self._level = 0
        self._score = 0
        self._board = self._create_empty_board()
        self._draw_new_piece()

    def _end(self):
        """
            Ends the game
        """
        self._is_over = True
        # self._restart()
        pass

    def get_copy(self):
        """
            Returns a copy of the current game

            Note : This function exists because other subclasses have
            non pickle-able attributes, preventing deepcopy to work...

            Returns
            -------
                TetrisBase
                    A perfect copy of the current game
        """
        copy = TetrisBase(self._params)
    
        #pp = pprint.PrettyPrinter(indent = 4)
        #pp.pprint(self.__dict__)

        copy._params = deepcopy(self._params)
        copy._random = deepcopy(self._random)
        copy._current_speed = deepcopy(self._current_speed)
        copy._current_time  = deepcopy(self._current_time)
        copy._board = deepcopy(self._board)
        copy._is_over = deepcopy(self._is_over)
        copy._level   = deepcopy(self._level)
        copy._score   = deepcopy(self._score)
        copy._lines_count = deepcopy(self._lines_count)
        copy._next_piece = deepcopy(self._next_piece)
        copy._current_piece = deepcopy(self._current_piece)
        copy._current_pos = deepcopy(self._current_pos)
        copy._store_piece = deepcopy(self._store_piece)
        
        #pp.pprint(copy.__dict__)

        return copy

    def try_moves(self, moves):
        """
            Try a set of moves until a piece is placed

            If moves contains too much elements, it will be trimmed to the one
            that actually placed the piece. If moves does not have enough
            elements, it is filled with DOWN action (to place the piece as 
            quickly as possible)

            Returns
            -------
                tuple
                    The set of move that places the piece, 
                    the resulting board (without boundaries), 
                    the new total number of lines cleared, 
                    the resulting score
        """
        m = deepcopy(moves)
        tetris_copy = self.get_copy()

        score = tetris_copy._score
        new_score = tetris_copy._score

        i = 0
        while score == new_score and not tetris_copy._is_over:
            if i < len(m):
                tetris_copy.tick(m[i])
            else:
                m.append(Controls.DOWN)
                tetris_copy.tick(Controls.DOWN)

            i = i + 1
            new_score = tetris_copy._score

        if i < len(m):
            m = m[:i]

        return m, deepcopy(tetris_copy._board[:-1, 1:-1]), tetris_copy._lines_count, tetris_copy._score