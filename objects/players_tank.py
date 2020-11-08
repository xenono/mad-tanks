import pygame

# Pre defined constant variables of speed X and Y
SPEED_X = 0.7
SPEED_Y = 0.7


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
        if direction == "UP":
            self.speed_y = -SPEED_Y
            if self.current_image_angle == 90 or self.current_image_angle == 270:
                self.position["y"] -= self.height / 3
            self.rotate_sprite("UP")

        if direction == "DOWN":
            self.speed_y = SPEED_Y
            self.rotate_sprite("DOWN")
        if direction == "RIGHT":
            self.speed_x = SPEED_X
            if self.current_image_angle == 0:
                self.position["y"] += self.height / 3
                self.position["x"] -= self.width / 4

            self.rotate_sprite("RIGHT")
            print(self.current_image_angle)

        if direction == "LEFT":
            self.speed_x = -SPEED_X
            if self.current_image_angle == 0:
                self.position["y"] += self.height / 3
                self.position["x"] -= self.width / 4
            self.rotate_sprite("LEFT")

    def update(self):
        # Moves sprite on x axis
        self.position["x"] += self.speed_x
        # Moves sprint on Y axis
        self.position["y"] += self.speed_y

    def stop(self):
        self.speed_x = self.speed_y = 0

    def rotate_sprite(self, direction):
        if direction == "UP":
            if self.current_image_angle == 0:
                return
            elif self.current_image_angle == 270:
                self.image = pygame.transform.rotate(self.image, 90)
                self.current_image_angle = 0
            elif abs(self.current_image_angle) == 180:
                self.image = pygame.transform.rotate(self.image, 180)
                self.current_image_angle = 0
            elif abs(self.current_image_angle) == 90:
                self.image = pygame.transform.rotate(self.image, -90)
                self.current_image_angle = 0
            return

        elif direction == "DOWN":
            if self.current_image_angle == 180:
                return
            elif self.current_image_angle == 0:
                self.image = pygame.transform.rotate(self.image, 180)
                self.current_image_angle = 180
            elif self.current_image_angle == 270:
                self.image = pygame.transform.rotate(self.image, 270)
                self.current_image_angle = 180
            elif self.current_image_angle == 90:
                self.image = pygame.transform.rotate(self.image, 90)
                self.current_image_angle = 180
            return

        elif direction == "RIGHT":
            if self.current_image_angle == 270:
                return
            elif self.current_image_angle == 0:
                self.image = pygame.transform.rotate(self.image, 270)
                self.current_image_angle = 270
            elif self.current_image_angle == 180:
                self.image = pygame.transform.rotate(self.image, 90)
                self.current_image_angle = 270
            elif self.current_image_angle == 90:
                self.image = pygame.transform.rotate(self.image, 180)
                self.current_image_angle = 270
            return
        elif direction == "LEFT":
            if self.current_image_angle == 90:
                return
            elif self.current_image_angle == 0:
                self.image = pygame.transform.rotate(self.image, 90)
                self.current_image_angle = 90
            elif self.current_image_angle == 180:
                self.image = pygame.transform.rotate(self.image, 270)
                self.current_image_angle = 90
            elif self.current_image_angle == 270:
                self.image = pygame.transform.rotate(self.image, 180)
                self.current_image_angle = 90
            return

