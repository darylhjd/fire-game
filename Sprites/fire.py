#! python3
# fire.py
"""CLass file for fire sprite"""

import random

import pygame
from pygame.sprite import Sprite


class Fire(Sprite):
    def __init__(self, screen, settings, firetruck, background):
        Sprite.__init__(self)
        self.settings = settings

        # Background settings
        self.background = background
        self.bg_rect = self.background.rect

        # Screen settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Firetruck
        self.firetruck = firetruck
        self.firetruck_rect = self.firetruck.rect

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(r"Images/fire.png").convert_alpha(), 0, 0.4)
        self.mask = pygame.mask.from_surface(self.image)

        # Position fire
        self.rect = self.image.get_rect()
        self.centerx = float(random.randint(self.firetruck_rect.right, self.bg_rect.right - 300))
        self.centery = float(random.randint(180, 465))
        self.rect.centery = self.centery

        # Movement
        self.xmove = self.background.xmove

    def check_speed(self, background):
        if background.rect.right <= self.settings.screen_width:
            self.xmove = 0

    def move_fire(self):
        self.centerx += self.xmove
        self.rect.centerx = self.centerx

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, background):
        self.check_speed(background)
        self.move_fire()
        self.blitme()
