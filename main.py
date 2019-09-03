#! python3
# main.py
# Firefighter game

import pygame
from pygame import DOUBLEBUF, HWSURFACE


class Settings:
    def __init__(self, width=1200, height=800):
        self.screen_width = width
        self.screen_height = height
        self.screen_dimensions = (self.screen_width, self.screen_height)


class Background:
    def __init__(self, screen, settings, picture):
        self.screen = screen
        self.settings = settings

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(picture).convert_alpha(), 0, 1)

        # Position Background
        self.rect = self.image.get_rect()
        self.topleft = (0, 0)
        self.rect.topleft = self.topleft


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
        self.fontobj = pygame.font.Font(font, size)
        self.surf = self.fontobj.render(self.msg, True, color, None)

        # Position
        self.rect = self.surf.get_rect()
        self.centerx = float(self.screen_rect.centerx)
        self.centery = float(self.screen_rect.centery - y_offset)


def start_screen(screen, settings):
    game_name = Message(screen, 64, "Fire Fire Pew", (250, 0, 0), 100)
    start = Message(screen, 24, "Press 'SPACE' to Start", (128, 128, 128), -100)
    bg = Background(screen, settings, r"Images/screen.png")

    while True:
        pass


def run_game():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_dimensions, DOUBLEBUF | HWSURFACE)
    pygame.display.set_caption("Pew Pew Fire")

    # Create font and stuff
    start_screen(screen, settings)
