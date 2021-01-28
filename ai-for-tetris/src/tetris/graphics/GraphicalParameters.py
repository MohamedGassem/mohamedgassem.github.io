import pygame
import json


def load_image(image):
    """
        Loads an image from a filepath

        If the argument is a string, this function is identical to
        pygame.image.load function.
        If the argument is a Surface, it just returns the surface
        If the argument is none of the above, returns an empty surface

        Parameters
        ----------
            image: any
                The source to build the image from

        Returns
        -------
            pygame.Surface
                A surface (that may be empty if a surface cannot be built from
                the argument)
    """
    if isinstance(image, pygame.Surface):
        return image

    try:
        surface = pygame.image.load(image)
        return surface
    except pygame.error as message:
        print("Cannot load : ", image)
        print("Reason : ", message)

        return pygame.Surface((0, 0))


def load_font(font, size):
    """
            Loads an image from a filepath

            If the argument is a string, this function is identical to
            pygame.image.load function.
            If the argument is a Surface, it just returns the surface
            If the argument is none of the above, returns an empty surface

            Parameters
            ----------
                font: any
                    The source to build the font from
                size: int
                    The size of the font in pixels

            Returns
            -------
                pygame.font.Font
                    A font (that may be 0-sized if a font cannot be built from
                    the argument)
        """
    if isinstance(font, pygame.font.Font):
        return font

    try:
        font = pygame.font.load(font, size)
        return font
    except pygame.error as message:
        print("Cannot load : ", font)
        print("Reason : ", message)

        return pygame.font.SysFont("arial", 0)


class GraphicalParameters:
    """
        Data class that holds all information about drawing the game

        Supported parameters are :
            background_pos : two int tuple
                Position of the background within a surface
            board_pos : two int tuple
                Position of the board within a surface
            next_pos : two int tuple
                Position of the upcoming piece within a surface
            stats_pos : two int tuple
                Positions of the game information within a surface
            block_size : two int tuple
                Size of each block, either on the board or the upcoming piece
            board_size : two int tuple
                Size of the board
            next_size : two int tuple
                Size of the upcoming piece
            stats_size: two int tuple
                Size of the game information
            background_image: pygame.Surface
                Background surface
            block_image : pygame.Surface
                Block image (whose size is block_size)
    """

    def __init__(self, **kwargs):
        """
            Ctor

            Parameters
            ----------
                kwargs: non positional argument dict
                    Supported parameters are :
                        background_pos : two int tuple
                            Position of the background within a surface
                        board_pos : two int tuple
                            Position of the board within a surface
                        next_pos : two int tuple
                            Position of the upcoming piece within a surface
                        info_pos : two int tuple
                            Positions of the game information within a surface
                        block_size : two int tuple
                            Size of each block, either on the board or the
                            upcoming piece
                        board_size : two int tuple
                            Size of the board
                        next_size : two int tuple
                            Size of the upcoming piece
                        info_size: two int tuple
                            Size of the game information
                        background_image: str or pygame.Surface
                            Background surface
                        block_image : str or pygame.Surface
                            Block image (will be automatically resized to
                            block_size)
                        main_font_size: int
                            The size of the main font
                        main_font: string or pygame.font.Font
                            The main font to use. Either a pre-loaded font or
                            a path to a TTF file
                        font_color: four int tuple
                            The color of the fonts
        """
        # Positions and dimensions

        # Position where to start drawing background
        self.background_pos = kwargs.get("background_pos", (0, 0))

        # Position where to start drawing the board
        self.board_pos = kwargs.get("board_pos", (0, 0))
        # Position where to draw the upcoming piece
        self.next_pos = kwargs.get("next_pos", (0, 0))
        # Position where to draw the statistics (points, level, ...)
        self.info_pos = kwargs.get("info_pos", (0, 0))

        # Size of each block
        self.block_size = kwargs.get("block_size", (0, 0))

        # Size of the board
        self.board_size = kwargs.get("board_size", (0, 0))
        # Size of the next piece rectangle
        self.next_size = kwargs.get("next_size", (0, 0))
        # Size of the statistic bounding box
        self.info_size = kwargs.get("info_size", (0, 0))

        # Images and fonts

        # Background
        self.background_image = load_image(
                    kwargs.get("background_image", pygame.Surface((0, 0)))
        )
        # Image to draw for each block
        self.block_image = load_image(
                    kwargs.get("block_image", pygame.Surface(self.block_size))
        )

        # The size parameter must be respected
        if self.block_image.get_size() != self.block_size:
            self.block_image = pygame.transform.scale(self.block_image,
                                                      self.block_size)

        self.main_font_size = kwargs.get("main_font_size", 15)
        self.main_font = load_font(
            kwargs.get("main_font", pygame.font.SysFont(
                "arial", self.main_font_size
            )),
            self.main_font_size
        )
        self.font_color = kwargs.get("font_color", (0, 0, 0, 255))


def parameter_from_json(json_file_path):
    """
        Loads graphical parameters from a json file

        Parameters
        ----------
            json_file_path: str
                The file path to the json file

        Returns
        -------
            tetris.graphics.GraphicalParameters
                An instance of tetris.graphics.GraphicalParameters built with
                the usable information in the json file
    """
    with open(json_file_path, 'r') as js_file:
        parameters = json.loads(js_file)
    return GraphicalParameters(**parameters)
