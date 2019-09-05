#! python3
# bg.py
"""Class fire for backgrounds in the game"""

import pygame


class Background:
    def __init__(self, screen, settings, picture, xmove=None):
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
        self.xmove = -self.settings.xmove if not xmove else -xmove

    def scroll(self):
        self.left += self.xmove
        self.rect.left = self.left

        # If bg right is less than zero, bring it back to the start
        if self.rect.right <= 0:
            self.left = 0
            self.rect.left = self.left

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, rep):  # If rep is false, then it is main background, else start screen background
        self.scroll()

        # If main background and end of bg, it will stop scrolling
        if not rep and self.rect.right < self.screen_rect.right:
            self.xmove = 0

        self.blitme()

        # If start background and bg right is less than screen width, draw another screen to loop
        if rep and self.rect.right < self.screen_rect.right:
            self.screen.blit(self.image, (self.rect.right, 0))
