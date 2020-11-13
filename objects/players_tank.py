import pygame

# Initial sprite dimensions
TANK_WIDTH = 50
TANK_HEIGHT = 76

# Pre defined constant variables of speed in each direction
SPEED = {
    "UP": -0.7,
    "DOWN": 0.7,
    "RIGHT": 0.7,
    "LEFT": -0.7
}

# Constant possible direction of movement direction : angle
DIRECTIONS = {
    "UP": 0,
    "LEFT": 90,
    "DOWN": 180,
    "RIGHT": 270
}


class PlayersTank:
    def __init__(self, position_x, position_y, screen):
        # Tank dimensions
        self.width = 50
        self.height = 76
        # Main game screen object
        self.screen = screen
        # Holds tank's position in dict
        self.position = {
            "x": position_x,
            "y": position_y
        }
        # Loads tank image
        self.image = pygame.image.load("assets/player_tank.png")
        # Tank speed
        self.speed_x = 0
        self.speed_y = 0
        # Holds current angle of image
        self.current_image_angle = 0

    def draw(self):
        # Draws tank on proper position
        self.screen.blit(self.image, (self.position["x"], self.position["y"]))

    def move(self, direction):
        # Changes speed according to the direction
        if direction == "UP" or direction == "DOWN":
            self.width = TANK_WIDTH
            self.height = TANK_HEIGHT
            self.speed_y = SPEED[direction]

            # Fix Y position caused rectangle sprite
            if self.current_image_angle == 270:
                self.position["x"] += 25

        elif direction == "RIGHT" or direction == "LEFT":
            # Swap dimensions (sprite is a rectangle)
            self.width = TANK_HEIGHT
            self.height = TANK_WIDTH
            self.speed_x = SPEED[direction]

            # Fix Y position caused rectangle sprite
            if self.current_image_angle == 180:
                self.position["y"] += 24

        # Rotates sprite
        self.rotate_sprite(direction)


    def update(self):
        # Moves sprite on x axis
        self.position["x"] += self.speed_x
        # Moves sprint on Y axis
        self.position["y"] += self.speed_y

    def stop(self):
        self.speed_x = self.speed_y = 0

    def rotate_sprite(self, destination_direction):
        # rotates image in appropriate direction
        if destination_direction == self.current_image_angle:
            self.current_image_angle = DIRECTIONS[destination_direction]
            return
        # Calculates angle difference
        rotate_angle = DIRECTIONS[destination_direction] - self.current_image_angle
        self.image = pygame.transform.rotate(self.image, rotate_angle)
        self.current_image_angle = DIRECTIONS[destination_direction]
