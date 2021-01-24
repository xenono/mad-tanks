import pygame

# Constant possible direction of movement direction : angle
DIRECTIONS = {
    "UP": 0,
    "LEFT": 90,
    "DOWN": 180,
    "RIGHT": 270
}


class Sprite:
    def __init__(self, screen, width, height, position_x, position_y, image_link, speed=0.3):
        # Sprite's dimensions
        self.__constWidth = width
        self.__constHeight = height
        self.__width = width
        self.__height = height
        # Holds Sprite's position in dict
        self.__position = {
            "x": position_x,
            "y": position_y
        }
        # Main game screen object
        self.__screen = screen
        # Loads Sprite's image
        self.__image = pygame.image.load(image_link)
        # Sprite speed values
        self.__speed_x = 0
        self.__speed_y = 0
        # Holds current angle of image to rotate when moving
        self.__current_image_angle = 0
        # Status of sprite's life
        self.__alive = True

        self.__speed_and_direction = {
            "UP": -speed,
            "DOWN": speed,
            "RIGHT": speed,
            "LEFT": -speed
        }

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def position(self):
        return self.__position

    @property
    def screen(self):
        return self.__screen

    @property
    def image(self):
        return self.__image

    @property
    def speed_x(self):
        return self.__speed_x

    @speed_x.setter
    def speed_x(self, value):
        self.__speed_x = value

    @property
    def speed_y(self):
        return self.__speed_y

    @speed_y.setter
    def speed_y(self, value):
        self.__speed_y = value

    @property
    def current_image_angle(self):
        return self.__current_image_angle

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, value):
        self.__alive = value

    @property
    def speed_and_direction(self):
        return self.__speed_and_direction

    def draw(self):
        # Draws sprite on proper position everytime when pygame loop executes
        self.screen.blit(self.image, (self.position["x"], self.position["y"]))

    def update(self):
        # Updates Sprite's values on game screen everytime when pygame loop executes
        # Moves sprite on x axis
        self.position["x"] += self.__speed_x
        # Moves sprite on Y axis
        self.position["y"] += self.__speed_y

    def move(self, direction):
        # Changes speed according to the direction
        if direction == "UP" or direction == "DOWN":
            self.__speed_y = self.speed_and_direction[direction]
            self.__speed_x = 0

            # Fix Y position caused rectangle sprite
            if direction == "DOWN" and self.current_image_angle == 90:
                self.position["x"] += 26
            elif direction == "UP" and self.current_image_angle == 90:
                self.position["x"] += 26
                self.position["y"] -= 26
            elif direction == "UP" and self.current_image_angle == 270:
                self.position["y"] -= 26

            # Swaps sprite dimensions
            if self.current_image_angle == 90 or self.current_image_angle == 270:
                self.__width = self.__constWidth
                self.__height = self.__constHeight

        elif direction == "RIGHT" or direction == "LEFT":
            # Swap dimensions (sprite is a rectangle)
            self.__speed_x = self.speed_and_direction[direction]
            self.__speed_y = 0

            # Fix Y position caused rectangle sprite
            if direction == "LEFT" and self.current_image_angle == 180:
                self.position["x"] -= 26
            elif direction == "LEFT" and self.current_image_angle == 0:
                self.position["x"] -= 26
                self.position["y"] += 26

            if direction == "RIGHT" and self.current_image_angle == 0:
                self.position["y"] += 26

            # Swaps sprite dimensions
            if self.current_image_angle == 0 or self.current_image_angle == 180:
                self.__width = self.__constHeight
                self.__height = self.__constWidth

        # Rotates sprite
        self.rotate_sprite(direction)

    def rotate_sprite(self, destination_direction):
        # rotates image in appropriate direction
        if destination_direction == self.current_image_angle:
            self.__current_image_angle = DIRECTIONS[destination_direction]
            return
        # Calculates angle difference
        rotate_angle = DIRECTIONS[destination_direction] - self.current_image_angle
        self.__image = pygame.transform.rotate(self.image, rotate_angle)
        self.__current_image_angle = DIRECTIONS[destination_direction]

    def stop(self, *args):
        self.__speed_x = self.__speed_y = 0

    def die(self):
        self.__alive = False
