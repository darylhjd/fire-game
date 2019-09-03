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
    def __init__(self, screen, settings, picture, xmove):
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

        # Movement
        self.xmove = -xmove

    def scroll(self):
        self.left += self.xmove
        self.rect.left = self.left

        if self.rect.right < 0:
            self.left = 0
            self.rect.left = self.left

    def update(self, rep):
        self.scroll()

        self.screen.blit(self.image, self.rect)
        if rep and self.rect.right < self.screen_rect.right:
            self.screen.blit(self.image, (self.rect.right, 0))


class FireTruck:
    def __init__(self, screen, settings, xmove):
        self.screen = screen
        self.settings = settings

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(r"Images/firetruck.png").convert_alpha(), 0, 0.5)
        self.mask = pygame.mask.from_surface(self.image)

        # Position Firetruck
        self.rect = self.image.get_rect()
        self.right = float(500)
        self.centery = float(650)
        self.rect.right = self.right
        self.rect.centery = self.centery

        # Movement
        self.xmove = xmove

    def move(self):
        self.right += self.xmove
        self.rect.right = self.right

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.move()
        self.blitme()


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

    def show_message(self):
        self.screen.blit(self.surf, self.rect)


def check_events(screen, space=False, q=False, pause=False):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if space and event.key == pygame.K_SPACE:
                return True
            if q and event.key == pygame.K_q:
                sys.exit()
            if pause and event.key == pygame.K_p:
                return pause_screen(screen)


def start_screen(screen, settings):
    game_name = Message(screen, 100, "Fire Fire Pew", (250, 0, 0), 100)
    start = Message(screen, 64, "Press 'SPACE' to murder some fires :)", (255, 102, 102), -200)
    bg = Background(screen, settings, r"Images/screen.png", 0.1)

    interval = 0
    while True:
        if check_events(screen, space=True, q=True, pause=False):
            del game_name, start
            break
        bg.update(True)
        game_name.show_message()
        if 0 <= interval <= 350:
            start.show_message()
            interval += 1
        else:
            interval += 1
            if interval == 700:
                interval = 0

        pygame.display.flip()


def pause_screen(screen):
    Message(screen, 100, "Game Paused", (0, 153, 0), 100).show_message()
    Message(screen, 50, "Press 'C' to continue, 'Q' to quit.", (0, 153, 0), -200).show_message()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:
                    return

                if event.key == pygame.K_q:
                    sys.exit()


def main_game(screen, settings):
    bg = Background(screen, settings, r"Images/BACKGROUND.png", 0.3)
    firetruck = FireTruck(screen, settings, 0.050)

    clock = pygame.time.Clock()

    while True:
        if check_events(screen, space=False, q=False, pause=True):
            break
        bg.update(False)
        firetruck.update()
        pygame.display.flip()

        clock.tick(140)


def run_game():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_dimensions, DOUBLEBUF | HWSURFACE)
    pygame.display.set_caption("Pew Pew Fire")

    # Start screen
    start_screen(screen, settings)

    # Main game
    main_game(screen, settings)


run_game()
