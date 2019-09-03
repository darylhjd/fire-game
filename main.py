#! python3
# main.py
# Firefighter game

import random
import sys

import pygame
from pygame import DOUBLEBUF, HWSURFACE
from pygame.sprite import Sprite, Group


class Settings:
    def __init__(self, width=1200, height=800):
        self.screen_width = width
        self.screen_height = height
        self.screen_dimensions = (self.screen_width, self.screen_height)

        # Screen settings
        self.xmove = 1

        # Fire settings
        self.fire_spawnchance = 0.01


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

        if self.rect.right < 0:
            self.left = 0
            self.rect.left = self.left

    def update(self, rep):
        if self.rect.right > self.screen_rect.right:
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


class Water(Sprite):
    def __init__(self, screen, settings, firetruck):
        Sprite.__init__(self)


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

        if self.rect.right < 0:
            self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, background):
        self.check_speed(background)
        self.move_fire()
        self.blitme()


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
    hmm = ['save some people',
           'solve global warming',
           'put out some fires',
           'save the cat on that tree',
           "drive a firetruck that isn't connected to a hydrant"]
    var = random.choice(hmm)

    game_name = Message(screen, 100, "Fire Fire Pew", (250, 0, 0), 100)
    start = Message(screen, 64, f"Press 'SPACE' to {var}", (255, 102, 102), -200)
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


# Linter please, I don't want to refactor this.
def end_screen(screen):
    Message(screen, 100, "Game End", (0, 153, 0), 100).show_message()
    Message(screen, 50, "Press 'R' to retry, 'E' to go to start screen, 'Q' to quit.",
            (0, 153, 0), -200).show_message()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return False

                if event.key == pygame.K_e:
                    return True

                if event.key == pygame.K_q:
                    sys.exit()


def create_fire(screen, settings, firetruck, background, fires):
    # Chance of spawning fire
    if random.random() <= settings.fire_spawnchance and background.rect.right > settings.screen_width:
        fire = Fire(screen, settings, firetruck, background)
        fires.add(fire)


def update_fires(screen, settings, firetruck, background, fires):
    create_fire(screen, settings, firetruck, background, fires)
    fires.update(background)


def main_game(screen, settings):
    bg = Background(screen, settings, r"Images/BACKGROUND.png")
    firetruck = FireTruck(screen, settings, 0.050)

    fires = Group()

    clock = pygame.time.Clock()

    while True:
        if check_events(screen, space=False, q=False, pause=True):
            break
        bg.update(False)
        update_fires(screen, settings, firetruck, bg, fires)
        firetruck.update(bg)
        pygame.display.flip()

        if firetruck.rect.left >= settings.screen_width:
            break
        clock.tick(140)


def initialise():
    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_dimensions, DOUBLEBUF | HWSURFACE)
    pygame.display.set_caption("Pew Pew Fire")

    return settings, screen


cont = True
r = True
pygame.init()

sett, scre = initialise()

while cont:
    if r:
        start_screen(scre, sett)

    main_game(scre, sett)
    r = end_screen(scre)
