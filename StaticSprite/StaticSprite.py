import pygame, math
from settings import Settings

# Constant possible direction of movement direction : angle
DIRECTIONS = {
    "UP": 0,
    "LEFT": 90,
    "DOWN": 180,
    "RIGHT": 270
}

settings = Settings()


class StaticSprite:
    """
        General Sprite class which has shared functions and attributes for every sprites which is on the screen.
    """

    def __init__(self, screen, position_x, position_y, image_link):
        # Calls constructor of pygame Sprite class.
        pygame.sprite.Sprite.__init__(self)
        # Holds Sprite's position in dict
        self.position = {
            "x": position_x,
            "y": position_y
        }
        # Main game screen object
        self.screen = screen
        # Loads Sprite's image
        self.image = pygame.image.load(image_link).convert_alpha()
        # Set position value to rect attribute which is required by pygame Group methods
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position["x"], self.position["y"]
        # Sprite's dimensions
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        # Status of sprite's life
        self.alive = True

    def draw(self):
        # Draws sprite on proper position everytime when pygame loop executes
        self.screen.blit(self.image, (self.position["x"], self.position["y"]))

    def update(self, *args):
        # Updates Sprite's values on game screen everytime when pygame loop executes
        # Updates the pygame's position values
        self.rect.x, self.rect.y = self.position["x"], self.position["y"]

    def die(self):
        self.alive = False
