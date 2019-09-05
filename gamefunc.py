#! python3
# gamefunc.py
"""Game functioss to run the main game"""

import random
import sys

import pygame
from pygame.sprite import Group

from Sprites.fire import Fire, FireGroup
from Sprites.firetruck import FireTruck
from Sprites.water import Water
from background import Background
from message import Message


def show_start_prompt(interval, start_prompt):
    interval += 1
    if 0 <= interval <= 100:
        start_prompt.show_message()
    else:
        if interval >= 200:
            interval = 0

    return interval


def start_screen(screen):
    prompts = ["save some people",
               "solve global warming",
               "put out some fires",
               "save the cat on that tree"]
    chosen_prompt = random.choice(prompts)

    picture_path = r'Images/screen.png'
    background = Background(screen, picture_path, speed=0.35, repeat=True)

    game_name = Message(screen, "Fire Pew Pew", (250, 0, 0), 100, size='big')
    start_prompt = Message(screen, f"Press 'SPACE' to {chosen_prompt}", (250, 0, 0), -200)

    clock = pygame.time.Clock()

    interval = 0
    while True:
        for event in pygame.event.get():
            full_quit(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        background.update()
        game_name.show_message()
        interval = show_start_prompt(interval, start_prompt)

        pygame.display.flip()
        clock.tick(140)


def show_water_left(screen, settings):
    water_left = Message(screen, f"Waters left: {settings.max_water}", (230, 0, 0), 0)
    water_left.rect.topleft = (0, 0)
    water_left.show_message()


def create_fire(screen, settings, fires, firetruck, background):
    fire = Fire(screen, settings, firetruck, background)
    fires.add(fire)
    fires.total_spawns += 1


def update_fire(screen, settings, fires, firetruck, background):
    # If chance and background is still scrolling
    if random.random() <= settings.fire_spawnchance and background.rect.right >= settings.screen_width:
        create_fire(screen, settings, fires, firetruck, background)

    fires.update(background)


def create_water(screen, settings, waters):
    coor = pygame.mouse.get_pos()
    water = Water(screen, settings, coor)
    settings.max_water -= 1
    waters.add(water)


def check_create_water(screen, settings, waters, event):
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and settings.max_water > 0:
        create_water(screen, settings, waters)


def main_game(screen, settings):  # NOSONAR
    picture_path = r"Images/BACKGROUND.png"
    background = Background(screen, picture_path, speed=settings.bg_speed, repeat=False)
    firetruck = FireTruck(screen, settings)

    fires = FireGroup()  # Special group to keep track of stats
    waters = Group()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p and pause_screen(screen):
                reset_game(settings, fires, waters)
                return

            # Create water when conditions are met
            check_create_water(screen, settings, waters, event)

        # Update background
        background.update()

        # Show number of water left
        show_water_left(screen, settings)

        # Update fire
        update_fire(screen, settings, fires, firetruck, background)

        # Update water
        waters.update(background)

        # Check water fire collisions
        pygame.sprite.groupcollide(waters, fires, False, True, collided=pygame.sprite.collide_mask)

        # Update firetruck and break if it leaves screen, ie. game ends
        if firetruck.update():
            score = (fires.total_spawns - len(fires)) / fires.total_spawns
            reset_game(settings, fires, waters)
            return score

        pygame.display.flip()
        clock.tick(140)


def reset_game(settings, *args):
    settings.max_water = 20
    for i in args:
        i.empty()


def end_screen(screen, score):
    Message(screen, "Game Over!", (0, 153, 0), 100, size='big').show_message()
    Message(screen, f"Your score is {round(score, 2)}", (0, 153, 0), -150, size="medium").show_message()
    Message(screen, "Press 'R' to retry, 'E' to go back to main menu, 'Q' to quit.", (0, 153, 0), -200).show_message()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            full_quit(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return False

                if event.key == pygame.K_e:
                    return True


def pause_screen(screen):
    Message(screen, "Gamed Paused", (0, 153, 0), 100, size='big').show_message()
    Message(screen, "Press 'Q' to quit, 'C' to continue, 'R' to retry", (0, 153, 0), -200).show_message()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            full_quit(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return

                if event.key == pygame.K_r:
                    return True


def full_quit(event):
    """This is used in end_screen() and start_screen()
    NOTE: This is not used in main_game() as conditions for quitting the game are different!"""

    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
        sys.exit()
