#! python3
# water.py
"""Class file for water sprite"""

import random

import pygame
from pygame.sprite import Sprite


class Water(Sprite):
    def __init__(self, screen, settings, firetruck, coor):
        Sprite.__init__(self)
        self.settings = settings

        # Screen settings
        self.screen = screen

        # Firetruck
        self.firetruck = firetruck
        self.ft_rect = self.firetruck.rect

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(r"Images/water.png").convert_alpha(),
                                               random.randint(0, 360), 0.2)
        self.mask = pygame.mask.from_surface(self.image)

        # Positioning
        self.rect = self.image.get_rect()
        self.rect.center = coor
        self.centerx = float(self.rect.centerx)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update_position(self, background):
        self.centerx += background.xmove
        self.rect.centerx = self.centerx

    def update(self, background):
        self.update_position(background)
        self.blitme()
