#! python3
# settings.py
"""Settings for main game"""


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
