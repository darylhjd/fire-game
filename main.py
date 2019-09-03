#! python3
# main.py
# Firefighter game

import sys

import pygame
from pygame import DOUBLEBUF, HWSURFACE


class Settings:
    def __init__(self, width=1200, height=800):
        self.screen_width = width
        self.screen_height = height
        self.screen_dimensions = (self.screen_width, self.screen_height)


class Background:
    def __init__(self, screen, settings, picture):
        self.settings = settings

        # Screen settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(picture).convert_alpha(), 0, 1)

        # Position Background
        self.rect = self.image.get_rect()
        self.left = float(0)
        self.centery = self.screen_rect.centery
        self.rect.left = self.left
        self.rect.centery = self.centery


class FireTruck:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(r"Images/firetruck.png").convert_alpha(), 0, 1)
        self.mask = pygame.mask.from_surface(self.image)

        # Position Firetruck
        self.rect = self.image.get_rect()
        self.left = float(200)
        self.centery = float(700)
        self.rect.left = self.left
        self.rect.centery = self.centery


class Fire:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(r"Images/fire.png").convert_alpha(), 0, 1)
        self.mask = pygame.mask.from_surface(self.image)


class Message:
    def __init__(self, screen, size, message, color, y_offset, font='comicsansms'):
        # Screen settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Font attributes
        self.size = size
        self.font = font
        self.msg = message

        # Font
        self.fontobj = pygame.font.SysFont(font, size)
        self.surf = self.fontobj.render(self.msg, True, color, None)

        # Position
        self.rect = self.surf.get_rect()
        self.centerx = float(self.screen_rect.centerx)
        self.centery = float(self.screen_rect.centery - y_offset)
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                return True
            if event.key == pygame.K_q:
                sys.exit()


def start_screen(screen, settings):
    game_name = Message(screen, 100, "Fire Fire Pew", (250, 0, 0), 100)
    start = Message(screen, 64, "Press 'SPACE' to Start", (255, 102, 102), -50)
    bg = Background(screen, settings, r"Images/screen.png")

    interval = 0
    while True:
        if check_events():
            break
        screen.blit(bg.image, bg.rect)
        screen.blit(game_name.surf, game_name.rect)
        if 0 <= interval <= 350:
            screen.blit(start.surf, start.rect)
            interval += 1
        else:
            interval += 1
            if interval == 700:
                interval = 0

        pygame.display.flip()


def run_game():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_dimensions, DOUBLEBUF | HWSURFACE)
    pygame.display.set_caption("Pew Pew Fire")

    # Start screen
    start_screen(screen, settings)


run_game()
