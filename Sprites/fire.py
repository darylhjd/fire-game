#! python3
# fire.py
"""CLass file for fire sprite"""

import random

import pygame
from pygame.sprite import Sprite, Group


class FireGroup(Group):
    def __init__(self):
        Group.__init__(self)

        self.total_spawns = 0


class Fire(Sprite):
    def __init__(self, screen, settings, firetruck, background):
        Sprite.__init__(self)
        self.settings = settings

        # Screen settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Background settings
        self.background = background
        self.background_rect = self.background.rect

        # Firetruck settings
        self.ft_rect = firetruck.rect
        self.ft_rect_left = self.ft_rect.left

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(r"Images/fire.png").convert_alpha(), 0, 0.4)
        self.mask = pygame.mask.from_surface(self.image)  # Mask for pixel-perfect collision.

        # Position fire
        self.rect = self.image.get_rect()
        self.centerx = float(random.randint(self.ft_rect_left, self.background_rect.right - 300))
        self.centery = float(random.randint(180, 465))
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        # Movement flags is decided in class methods. This makes sure that the speed is always equal to
        # that of the background.

    def move(self, background):
        self.centerx -= background.xmove
        self.rect.centerx = self.centerx

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, background):
        self.move(background)
        self.blitme()
