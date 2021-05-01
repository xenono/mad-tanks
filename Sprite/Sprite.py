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


class Sprite:
    """
        General Sprite class which has shared functions and attributes for every sprites which is on the screen.
    """

    def __init__(self, screen, width, height, position_x, position_y, image_link, speed=0.3):
        # Calls constructor of pygame Sprite class.
        pygame.sprite.Sprite.__init__(self)

        # Sprite's dimensions
        self.constWidth = width
        self.constHeight = height
        self.width = width
        self.height = height
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

        # Sprite speed values
        self.speed_x = 0
        self.speed_y = 0
        # Holds current angle of image to rotate when moving
        self.current_image_angle = 0
        # Status of sprite's life
        self.alive = True

        self.speed_and_direction = {
            "UP": -speed,
            "DOWN": speed,
            "RIGHT": speed,
            "LEFT": -speed
        }

    def draw(self):
        # Draws sprite on proper position everytime when pygame loop executes
        self.screen.blit(self.image, (self.position["x"], self.position["y"]))

    def update(self, *args):
        # Updates Sprite's values on game screen everytime when pygame loop executes
        # Moves sprite on x axis
        self.position["x"] += self.speed_x
        # Moves sprite on Y axis
        self.position["y"] += self.speed_y
        # Updates the pygame's position values
        self.rect.x, self.rect.y = self.position["x"], self.position["y"]

    def move(self, direction):
        # Changes speed according to the direction
        if direction == "UP" or direction == "DOWN":
            self.speed_y = self.speed_and_direction[direction]
            self.speed_x = 0

            # Fix Y position caused rectangle sprite
            if direction == "DOWN" and self.current_image_angle == 90:
                self.position["x"] += self.height / 2 + 1
            elif direction == "UP" and self.current_image_angle == 90:
                self.position["x"] += self.height / 2 + 1
                self.position["y"] -= self.height / 2 + 1
            elif direction == "UP" and self.current_image_angle == 270:
                self.position["y"] -= self.height / 2 + 1

            # Swaps sprite dimensions
            if self.current_image_angle == 90 or self.current_image_angle == 270:
                self.width = self.constWidth
                self.rect.width = self.constWidth
                self.height = self.constHeight
                self.rect.height = self.constHeight

        elif direction == "RIGHT" or direction == "LEFT":
            # Swap dimensions (sprite is a rectangle)
            self.speed_x = self.speed_and_direction[direction]
            self.speed_y = 0

            # Fix Y position caused rectangle sprite
            if direction == "LEFT" and self.current_image_angle == 180:
                self.position["x"] -= self.width / 2 + 1
            elif direction == "LEFT" and self.current_image_angle == 0:
                self.position['x'] -= self.width / 2 + 1
                self.position["y"] += self.width / 2 + 1

            if direction == "RIGHT" and self.current_image_angle == 0:
                self.position["y"] += self.width / 2 + 1

            # Swaps sprite dimensions
            if self.current_image_angle == 0 or self.current_image_angle == 180:
                self.width = self.constHeight
                self.rect.width = self.constHeight
                self.height = self.constWidth
                self.rect.height = self.constWidth

        # Rotates sprite
        self.rotate_sprite(direction)

    def rotate_sprite(self, destination_direction):
        # rotates image in appropriate direction
        if destination_direction == self.current_image_angle:
            self.current_image_angle = DIRECTIONS[destination_direction]
            return
        # Calculates angle difference
        rotate_angle = DIRECTIONS[destination_direction] - self.current_image_angle
        self.image = pygame.transform.rotate(self.image, rotate_angle)
        self.current_image_angle = DIRECTIONS[destination_direction]

    def stop(self, *args):
        self.speed_x = self.speed_y = 0

    def die(self):
        self.alive = False
