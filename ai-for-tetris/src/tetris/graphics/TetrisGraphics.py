import pygame
from src.tetris.base.Controls import Controls
from src.tetris.base.TetrisBase import TetrisBase


class TetrisGraphics(TetrisBase):
    """
        Class that display in a pygame surface a Tetris game
    """
    # Clear color for surfaces, may help for debugging display areas
    CLEAR_COLOR = (0, 0, 0, 0)

    def __init__(self, graphical_params, game_params):
        """
            Ctor

            Parameters
            ----------
                graphical_params: GraphicalParameters
                    The display parameters for the game. See
                    src.tetris.graphics.GraphicalParameters for more information
                    about those parameters.
                game_params: GameParameters
                    Parameters for the game. See class documentation for more
                    details
        """
        super().__init__(game_params)

        # Movement timers
        self._mvt_ticks_speed = 5
        self._left_timer = self._mvt_ticks_speed
        self._right_timer = self._mvt_ticks_speed
        self._down_timer = self._mvt_ticks_speed

        self._gparams = graphical_params
        # Activate alpha on surface to have the background above the board
        self._board_surface = pygame.Surface(
            self._gparams.board_size, pygame.SRCALPHA, 32
        )
        self._board_surface = self._board_surface.convert_alpha()

        self._info_surface = pygame.Surface(
            self._gparams.info_size, pygame.SRCALPHA, 32
        )
        self._info_surface = self._info_surface.convert_alpha()

        self._next_surface = pygame.Surface(
            self._gparams.next_size, pygame.SRCALPHA, 32
        )
        self._next_surface = self._next_surface.convert_alpha()

    def _on_draw_board(self):
        """
            Draws the game on the designated surface
        """
        # Clear surface
        self._board_surface.fill(TetrisGraphics.CLEAR_COLOR)

        # Remove boundaries
        current_board = self.get_current_game_state()
        current_board = current_board[:-1, 1:-1]

        size_x = self._gparams.block_size[0]
        size_y = self._gparams.block_size[1]

        for i in range(current_board.shape[0]):
            pos_y = i * size_y

            for j in range(current_board.shape[1]):
                pos_x = j * size_x
                rect = (pos_x, pos_y, size_x, size_y)

                if current_board[i][j] != 0:
                    self._board_surface.blit(self._gparams.block_image, rect)

    def _on_draw_info(self):
        """
            Draws the information (level, score, ...) about the game
        """

        # Clear surface
        self._info_surface.fill(TetrisGraphics.CLEAR_COLOR)

        # TODO : Extract offset to graphical parameters
        starting_pos = (0, 0)

        # TODO : Extract texts to resource file
        # TODO : Pre-load non-changing font textures
        # TODO : Extract display functions
        level_display_text = "Level"
        level_display_size = self._gparams.main_font.size(level_display_text)
        level_display_surface = self._gparams.main_font.render(
            level_display_text, True, self._gparams.font_color
        )

        center_x = self._gparams.info_size[0] / 2 - level_display_size[0] / 2
        starting_pos = (center_x, starting_pos[1])

        level_count_text = str(self._level + 1)
        level_count_size = self._gparams.main_font.size(level_count_text)
        level_count_surface = self._gparams.main_font.render(
            level_count_text, True, self._gparams.font_color
        )

        center_x = self._gparams.info_size[0] / 2 - level_count_size[0] / 2
        level_count_pos = (center_x, starting_pos[1] + level_display_size[1])

        score_display_text = "Score"
        score_display_size = self._gparams.main_font.size(score_display_text)
        score_display_surface = self._gparams.main_font.render(
            score_display_text, True, self._gparams.font_color
        )

        center_x = self._gparams.info_size[0] / 2 - score_display_size[0] / 2
        score_display_pos = (center_x,
                             level_count_pos[1] + score_display_size[1])

        score_value_text = str(self._score)
        score_value_size = self._gparams.main_font.size(score_value_text)
        score_value_surface = self._gparams.main_font.render(
            score_value_text, True, self._gparams.font_color
        )

        center_x = self._gparams.info_size[0] / 2 - score_value_size[0] / 2
        score_value_pos = (center_x,
                           level_count_pos[1] + score_display_pos[1])

        line_display_text = "Line"
        line_display_size = self._gparams.main_font.size(line_display_text)
        line_display_surface = self._gparams.main_font.render(
            line_display_text, True, self._gparams.font_color
        )

        center_x = self._gparams.info_size[0] / 2 - line_display_size[0] / 2
        line_display_pos = (center_x,
                            score_value_pos[1] + line_display_size[1])

        line_value_text = str(self._lines_count)
        line_value_size = self._gparams.main_font.size(line_value_text)
        line_value_surface = self._gparams.main_font.render(
            line_value_text, True, self._gparams.font_color
        )

        center_x = self._gparams.info_size[0] / 2 - line_value_size[0] / 2
        line_value_pos = (center_x,
                          level_count_pos[1] + line_display_pos[1])

        self._info_surface.blit(level_display_surface, starting_pos)
        self._info_surface.blit(level_count_surface, level_count_pos)
        self._info_surface.blit(score_display_surface, score_display_pos)
        self._info_surface.blit(score_value_surface, score_value_pos)
        self._info_surface.blit(line_display_surface, line_display_pos)
        self._info_surface.blit(line_value_surface, line_value_pos)

    def _on_draw_next(self):
        """
            Draws the upcoming piece
        """
        self._next_surface.fill(TetrisGraphics.CLEAR_COLOR)

        _, piece_data = self._next_piece.compute_current_bounds()
        piece_size = piece_data.shape

        surface_size = (piece_size[1] * self._gparams.block_size[1],
                        piece_size[0] * self._gparams.block_size[0])

        next_surface = pygame.Surface(surface_size, pygame.SRCALPHA, 32)
        next_surface = next_surface.convert_alpha()

        for i in range(piece_size[0]):
            pos_y = i * self._gparams.block_size[1]

            for j in range(piece_size[1]):
                pos_x = j * self._gparams.block_size[0]

                if piece_data[i][j] != 0:
                    next_surface.blit(self._gparams.block_image, (pos_x, pos_y))

        # Preserve aspect ratio
        ratio = min(0.75 * self._gparams.next_size[0] / surface_size[0],
                    0.75 * self._gparams.next_size[1] / surface_size[1])
        ratio = min(ratio, 1)

        dest_size = (int(ratio * surface_size[0]),
                     int(ratio * surface_size[1]))
        next_surface = pygame.transform.scale(next_surface, dest_size)

        center = (self._gparams.next_size[0] / 2,
                  self._gparams.next_size[1] / 2)
        dest_pos = (center[0] - dest_size[0] / 2, center[1] - dest_size[1] / 2)

        self._next_surface.blit(next_surface, dest_pos)

    def on_update(self, events):
        """
            Updates the game according to the event
        """
        mvt = Controls.NOTHING

        # Non-repeatable actions
        # Keeping the key down won't trigger multiple time those action
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'a':
                    mvt = Controls.ROTATE_LEFT
                elif event.unicode == 'e':
                    mvt = Controls.ROTATE_RIGHT

        # Repeatable actions
        # Maintain timer so the action isn't done every tick
        keys = pygame.key.get_pressed()
        # With this method keycodes are used hence the keyboard layout is
        # defaulted to qwerty
        if keys[pygame.K_a]:
            if self._left_timer >= self._mvt_ticks_speed:
                mvt = Controls.LEFT
                self._left_timer = 0
            else:
                self._left_timer += 1
        elif keys[pygame.K_d]:
            if self._right_timer >= self._mvt_ticks_speed:
                mvt = Controls.RIGHT
                self._right_timer = 0
            else:
                self._right_timer += 1
        elif keys[pygame.K_s]:
            if self._down_timer >= self._mvt_ticks_speed:
                mvt = Controls.DOWN
                self._down_timer = 0
            else:
                self._down_timer += 1

        self.tick(mvt)

    def on_draw(self, surface):
        """
            Draws the game on the given surface

            Note : the coherence between the surface and other parameters
            (positions, dimensions, ...) is not checked.

            Parameters
            ----------
                surface: pygame.Surface
                    The surface to blit into
        """
        self._on_draw_board()
        self._on_draw_info()
        self._on_draw_next()

        surface.blit(
            self._gparams.background_image, self._gparams.background_pos
        )
        surface.blit(self._board_surface, self._gparams.board_pos)
        surface.blit(self._info_surface, self._gparams.info_pos)
        surface.blit(self._next_surface, self._gparams.next_pos)