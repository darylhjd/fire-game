#! python3
# main.py
# Firefighter game

import pygame
from pygame import DOUBLEBUF, HWSURFACE

from gamefunctions import start_screen, main_game, end_screen
from settings import Settings


def main():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_dimensions, DOUBLEBUF | HWSURFACE)
    pygame.display.set_caption("Do You Like FireTrucks?")

    return_to_start = True  # Initialise True to make start_screen run on first run
    while True:
        if return_to_start:
            start_screen(screen, settings)

        score = main_game(screen, settings)
        return_to_start = end_screen(screen, score)


main()
