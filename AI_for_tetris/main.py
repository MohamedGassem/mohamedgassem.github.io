import pygame
from src.Application import Application

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    app = Application()
    app.run()

    pygame.quit()
