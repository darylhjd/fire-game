#! python3
# gamefunctions.py
"""Functions to run the main game"""
import random
import sys

import pygame
from pygame.sprite import Group

from Sprites.fire import Fire
from Sprites.firetruck import FireTruck
from Sprites.water import Water
from background import Background
from message import Message


def main_water_event(screen, settings, firetruck, background, waters):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                pause_screen(screen)

            if event.key == pygame.K_b and settings.max_water > 0:
                coor = pygame.mouse.get_pos()
                water = Water(screen, settings, firetruck, coor)
                waters.add(water)
                settings.max_water -= 1

    waters.update(background)


def main_game(screen, settings):
    bg = Background(screen, settings, r"Images/BACKGROUND.png")
    firetruck = FireTruck(screen, settings, 0.050)

    fires = Group()
    total_fires = 0

    waters = Group()

    clock = pygame.time.Clock()

    while True:
        main_water_event(screen, settings, firetruck, bg, waters)

        if update_fires(screen, settings, firetruck, bg, fires):
            total_fires += 1

        # Check collisions
        pygame.sprite.groupcollide(waters, fires, False, True, collided=pygame.sprite.collide_mask)

        firetruck.update(bg)

        pygame.display.flip()

        if firetruck.rect.left >= settings.screen_width:
            score = (total_fires - len(fires)) / total_fires
            fires.empty()
            waters.empty()
            settings.max_water = 20
            return score

        clock.tick(140)
