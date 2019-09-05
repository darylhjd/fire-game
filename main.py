#! python3
# main.py
# Firefighter game

import pygame
from pygame import DOUBLEBUF, HWSURFACE

from gamefunc import start_screen, main_game, end_screen
from settings import Settings


def main():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_dimensions, DOUBLEBUF | HWSURFACE)
    pygame.display.set_caption("Do You Like FireTrucks?")

    return_to_start = True  # Initialise True to make start_screen run on first run
    while True:
        if return_to_start:
            start_screen(screen)

        score = main_game(screen, settings)
        if score is None:  # If player restarts while in the middle of the game
            return_to_start = False
            continue

        return_to_start = end_screen(screen, score)  # If return_to_start is False, restart to main_game immediately


main()
