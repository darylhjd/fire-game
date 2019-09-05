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
from bg import Background
from message import Message


def start_screen_eventloop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                return True

            if event.key == pygame.K_q:
                sys.exit()


def start_screen(screen, settings):
    hmm = ['save some people',
           'solve global warming',
           'put out some fires',
           'save the cat on that tree']
    var = random.choice(hmm)

    game_name = Message(screen, 60, "Fire Fire Pew", (250, 0, 0), 100)
    start = Message(screen, 30, f"Press 'SPACE' to {var}", (255, 102, 102), -200)
    bg = Background(screen, settings, r"Images/screen.png", 0.1)

    interval = 0
    while True:
        if start_screen_eventloop():
            break

        bg.update(True)
        game_name.show_message()

        interval += 1
        if 0 <= interval <= 350:
            start.show_message()
        else:
            if interval == 700:
                interval = 0

        pygame.display.flip()


def pause_screen(screen):  # NOSONAR
    Message(screen, 60, "Game Paused", (0, 153, 0), 100).show_message()
    Message(screen, 30, "Press 'C' to continue, 'Q' to quit.", (0, 153, 0), -200).show_message()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:
                    return

                if event.key == pygame.K_q:
                    sys.exit()


def end_screen_eventloop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                return False

            if event.key == pygame.K_e:
                return True

            if event.key == pygame.K_q:
                sys.exit()


def end_screen(screen, score):
    Message(screen, 60, "Game End", (0, 153, 0), 100).show_message()
    Message(screen, 30, "Your score is: {:.2f}".format(score), (0, 153, 0), -150).show_message()
    Message(screen, 25, "Press 'R' to retry, 'E' to go to start screen, 'Q' to quit.",
            (0, 153, 0), -200).show_message()
    pygame.display.flip()

    while True:
        moveon = end_screen_eventloop()

        if moveon is not None:
            return moveon


def create_fire(screen, settings, firetruck, background, fires):
    # Chance of spawning fire
    created = False
    if random.random() <= settings.fire_spawnchance and background.rect.right > settings.screen_width:
        fire = Fire(screen, settings, firetruck, background)
        fires.add(fire)
        created = True

    fires.update(background)
    return created


def update_fires(screen, settings, firetruck, background, fires):
    return create_fire(screen, settings, firetruck, background, fires)


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


def show_water_left(screen, settings):
    msg = Message(screen, 25, f"Waters left: {settings.max_water}", (230, 0, 0), 0)
    msg.rect.topleft = (0, 0)
    msg.show_message()


def main_game(screen, settings):
    bg = Background(screen, settings, r"Images/BACKGROUND.png")
    firetruck = FireTruck(screen, settings, 0.050)

    fires = Group()
    total_fires = 0

    waters = Group()

    clock = pygame.time.Clock()

    while True:
        bg.update(False)
        show_water_left(screen, settings)

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
