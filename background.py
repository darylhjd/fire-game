#! python3
# background.py
"""Class fire for backgrounds in the game"""

import pygame


class Background:
    def __init__(self, screen, picture_path, speed=0, repeat=False):

        # Screen settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Image
        self.image = pygame.image.load(picture_path).convert_alpha()

        # Position background
        self.rect = self.image.get_rect()
        self.left = float(0)
        self.centery = float(self.screen_rect.centery)
        self.rect.left = self.left
        self.rect.centery = self.centery

        # Movement flags
        self.to_repeat = repeat
        self.xmove = speed

    def scroll(self):
        if self.rect.right <= self.screen_rect.right and not self.to_repeat:
            self.xmove = 0

        self.left -= self.xmove
        self.rect.left = self.left

    def blitme(self):
        self.screen.blit(self.image, self.rect)

        if self.rect.right < self.screen_rect.right:
            self.screen.blit(self.image, (self.rect.right, 0))

    def update(self):
        self.scroll()
        self.blitme()
