#! python3
# firetruck.py
"""Class file for the Firetruck"""

import pygame


class FireTruck:
    def __init__(self, screen, settings):
        self.settings = settings

        # Screen settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(r"Images/firetruck.png").convert_alpha(), 0, 0.5)

        # Position Firetruck
        self.rect = self.image.get_rect()
        self.right = float(500)
        self.centery = float(650)
        self.rect.right = self.right
        self.rect.centery = self.centery

        # Movement flags
        self.xmove = self.settings.truck_xmove

    def move(self):
        self.right += self.xmove
        self.rect.right = self.right

        if self.rect.right >= self.screen_rect.right + 20:
            return True

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.blitme()
        if self.move():
            return True
