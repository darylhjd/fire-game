#! python3
# ONEFILE.py
"""Long files look impressive lol"""

import random
import sys

import pygame
from pygame import DOUBLEBUF, HWSURFACE
from pygame.sprite import Sprite, Group


class Message:
    def __init__(self, screen, message, color, y_offset, size='small', font='comicsansms'):
        # Screen settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Size
        if size == 'small':
            self.size = 25
        elif size == 'medium':
            self.size = 30
        elif size == 'big':
            self.size = 50

        # Font
        self.fontobj = pygame.font.SysFont(font, int(self.size * self.screen_rect.width / self.screen_rect.height))
        self.surf = self.fontobj.render(message, True, color, None)  # Antialias True, no background

        # Position
        self.rect = self.surf.get_rect()
        self.centerx = float(self.screen_rect.centerx)
        self.centery = float(self.screen_rect.centery - y_offset)
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def show_message(self):
        self.screen.blit(self.surf, self.rect)


class Settings:
    def __init__(self, width=1200, height=800):
        self.screen_width = width
        self.screen_height = height
        self.screen_dimensions = (self.screen_width, self.screen_height)

        # Background settings
        self.bg_speed = 1

        # Firetruck settings
        self.truck_xmove = 0.165

        # Fire settings
        self.fire_spawnchance = 0.01

        # Water settings
        self.max_water = 20


class Background:
    def __init__(self, screen, picture_path, speed=float(0), repeat=False):

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


class Water(Sprite):
    def __init__(self, screen, settings, coor):
        Sprite.__init__(self)
        self.settings = settings

        # Screen settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Image
        self.image = pygame.transform.rotozoom(pygame.image.load(r"Images/water.png").convert_alpha(),
                                               random.randint(0, 360), 0.2)
        self.mask = pygame.mask.from_surface(self.image)

        # Positioning
        self.rect = self.image.get_rect()
        self.rect.center = coor
        self.centerx = float(self.rect.centerx)

        # Like Fire, Water's movement is decided in the class methods to ensure parity with the background.

    def move(self, background):
        self.centerx -= background.xmove
        self.rect.centerx = self.centerx

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, background):
        self.move(background)
        self.blitme()


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


def show_start_prompt(interval, start_prompt):
    interval += 1
    if 0 <= interval <= 100:
        start_prompt.show_message()
    else:
        if interval >= 200:
            interval = 0

    return interval


def start_screen(screen):
    prompts = ["save some people",
               "solve global warming",
               "put out some fires",
               "save the cat on that tree"]
    chosen_prompt = random.choice(prompts)

    picture_path = r'Images/screen.png'
    background = Background(screen, picture_path, speed=0.35, repeat=True)

    game_name = Message(screen, "Fire Pew Pew", (250, 0, 0), 100, size='big')
    start_prompt = Message(screen, f"Pess 'SPACE' to {chosen_prompt}", (250, 0, 0), -200)

    clock = pygame.time.Clock()

    interval = 0
    while True:
        for event in pygame.event.get():
            full_quit(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        background.update()
        game_name.show_message()
        interval = show_start_prompt(interval, start_prompt)

        pygame.display.flip()
        clock.tick(140)


def show_water_left(screen, settings):
    water_left = Message(screen, f"Waters left: {settings.max_water}", (230, 0, 0), 0)
    water_left.rect.topleft = (0, 0)
    water_left.show_message()


def create_fire(screen, settings, fires, firetruck, background):
    fire = Fire(screen, settings, firetruck, background)
    fires.add(fire)
    fires.total_spawns += 1


def update_fire(screen, settings, fires, firetruck, background):
    # If chance and background is still scrolling
    if random.random() <= settings.fire_spawnchance and background.rect.right >= settings.screen_width:
        create_fire(screen, settings, fires, firetruck, background)

    fires.update(background)


def create_water(screen, settings, waters):
    coor = pygame.mouse.get_pos()
    water = Water(screen, settings, coor)
    settings.max_water -= 1
    waters.add(water)


def check_create_water(screen, settings, waters, event):
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and settings.max_water > 0:
        create_water(screen, settings, waters)


def main_game(screen, settings):  # NOSONAR
    picture_path = r"Images/BACKGROUND.png"
    background = Background(screen, picture_path, speed=settings.bg_speed, repeat=False)
    firetruck = FireTruck(screen, settings)

    fires = FireGroup()  # Special group to keep track of stats
    waters = Group()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p and pause_screen(screen):
                reset_game(settings, fires, waters)
                return

            # Create water when conditions are met
            check_create_water(screen, settings, waters, event)

        # Update background
        background.update()

        # Show number of water left
        show_water_left(screen, settings)

        # Update fire
        update_fire(screen, settings, fires, firetruck, background)

        # Update water
        waters.update(background)

        # Check water fire collisions
        pygame.sprite.groupcollide(waters, fires, False, True, collided=pygame.sprite.collide_mask)

        # Update firetruck and break if it leaves screen, ie. game ends
        if firetruck.update():
            score = (fires.total_spawns - len(fires)) / fires.total_spawns
            reset_game(settings, fires, waters)
            return score

        pygame.display.flip()
        clock.tick(140)


def reset_game(settings, *args):
    settings.max_water = 20
    for i in args:
        i.empty()


def end_screen(screen, score):
    Message(screen, "Game Over!", (0, 153, 0), 100, size='big').show_message()
    Message(screen, f"Your score is {round(score, 2)}", (0, 153, 0), -150, size="medium").show_message()
    Message(screen, "Press 'R' to retry, 'E' to go back to main menu, 'Q' to quit.", (0, 153, 0), -200).show_message()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            full_quit(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return False

                if event.key == pygame.K_e:
                    return True


def pause_screen(screen):
    Message(screen, "Gamed Paused", (0, 153, 0), 100, size='big').show_message()
    Message(screen, "Press 'Q' to quit, 'C' to continue, 'R' to retry", (0, 153, 0), -200).show_message()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            full_quit(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return

                if event.key == pygame.K_r:
                    return True


def full_quit(event):
    """This is used in end_screen() and start_screen()
    NOTE: This is not used in main_game() as conditions for quitting the game are different!"""

    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
        sys.exit()


def main():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_dimensions, DOUBLEBUF | HWSURFACE)
    pygame.display.set_caption("Do You Like FireTrucks?")

    return_to_start = True  # Initialise True to make start_screen run on first run
    while True:
        if return_to_start:
            start_screen(screen)

        score = main_game(screen, settings)
        if score is None:  # If player restarts while in the middle of the game
            return_to_start = False
            continue

        return_to_start = end_screen(screen, score)  # If return_to_start is False, restart to main_game immediately


main()
