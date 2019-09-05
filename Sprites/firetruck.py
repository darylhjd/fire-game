#! python3
# firetruck.py
"""Class file for the Firetruck"""

import pygame


class FireTruck:
    def __init__(self, screen, settings, xmove):
        self.screen = screen
        self.settings = settings

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(r"Images/firetruck.png").convert_alpha(), 0, 0.5)

        # Position Firetruck
        self.rect = self.image.get_rect()
        self.right = float(500)
        self.centery = float(650)
        self.rect.right = self.right
        self.rect.centery = self.centery

        # Movement
        self.increase_speed = False
        self.xmove = xmove

    def check_increase(self, background):
        if background.rect.right <= self.settings.screen_width:
            self.xmove += self.settings.xmove/2

    def move(self):
        self.right += self.xmove
        self.rect.right = self.right

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, background):
        self.check_increase(background)
        self.move()
        self.blitme()
