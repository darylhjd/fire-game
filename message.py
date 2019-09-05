#! python3
# message.py
"""Class file for messages in the game"""

import pygame


class Message:
    def __init__(self, screen, size, message, color, y_offset, font='comicsansms'):
        # Screen settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Font
        self.fontobj = pygame.font.SysFont(font, int(size*self.screen_rect.width/self.screen_rect.height))
        self.surf = self.fontobj.render(message, True, color, None)

        # Position
        self.rect = self.surf.get_rect()
        self.centerx = float(self.screen_rect.centerx)
        self.centery = float(self.screen_rect.centery - y_offset)
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def show_message(self):
        self.screen.blit(self.surf, self.rect)
