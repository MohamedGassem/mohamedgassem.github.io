import pygame
import numpy as np

from src.pieces import *

from src.AI.GeneticAlgorithm import GeneticAlgorithm
from src.AI.GeneticAlgorithm import GeneticAlgorithmParameters
from src.AI.GeneticAlgorithm import GeneticAlgorithmStatistics 

from src.AI.QLearning import QLearningAI
from src.AI.LookupAI import LookupAI
from src.AI.NEAT import NEATAI

from src.tetris.base.GameParameters import GameParameters
from src.tetris.graphics.TetrisGraphics import TetrisGraphics
from src.tetris.graphics.GraphicalParameters import GraphicalParameters
from src.tetris.graphics.TetrisGraphicsBinder import TetrisGraphicsBinder

from src.AI.Random import RandomAI
from src.AI.QLearning import QLearningAI

class Application:
    """
        Class holding the windows and setting up game
    """

    def __init__(self):
        """
            Ctor
        """
        mode = pygame.HWSURFACE | pygame.DOUBLEBUF
        self._main_window = pygame.display.set_mode((600, 800), mode)

        # TODO : Load from external file
        self._game_params = GameParameters(
            pieces=CLASSICAL_PIECES, 
        )
        self._graphical_params = GraphicalParameters(
            board_pos=(42, 47),
            board_size=(332, 704),
            background_image="res/background.png",
            background_pos=(0, 0),
            block_image="res/block_image.png",
            block_size=(33, 35),
            info_pos=(421, 249),
            info_size=(149, 505),
            next_pos=(421, 49),
            next_size=(149, 167),
            main_font_size=30
        )

        AI = LookupAI(self._game_params, GeneticAlgorithmParameters())
        AI._coeffs = [-0.5, 0.7, -0.35, -0.18]
    
        if False:
            self._game = TetrisGraphics(
                self._graphical_params, self._game_params
            )
        else:  
            self._game = TetrisGraphicsBinder(
                AI.predict, self._graphical_params, self._game_params
            )
            AI.bind(self._game)

    def run(self):
        """
            Run the application

            Note : This function will block the current thread and will
            terminate when closing the window
        """
        running = True

        while running:
            # One update every 16 ms (60 fps)
            # pygame.time.wait(int(1000 / 60))
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            self._update(events)
            self._draw()

    def _update(self, events):
        """
            Update the application

            Parameters
            ----------
                events: array_like of pygame.event
                    The events for the current frame
        """
        # Update the game
        self._game.on_update(events)

    def _draw(self):
        """
            Draws the application components
        """
        # Clears the screen
        self._main_window.fill((255, 255, 255, 255))

        # Draws the game
        self._game.on_draw(self._main_window)

        # Swaps buffers
        pygame.display.flip()
