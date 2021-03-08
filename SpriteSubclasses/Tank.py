import pygame, math
from Sprite.Sprite import Sprite
from SpriteSubclasses.TankBullet import TankBullet
from GifAnimation.GifAnimation import GifAnimation
from settings import Settings

settings = Settings()


class Tank(Sprite):
    """
        This class provides functions and attributes required for player's and enemy's tank sprite.
    """

    def __init__(self, position_x, position_y, screen):
        super().__init__(screen, settings.tankWidth, settings.tankHeight, position_x, position_y,
                         "assets/square.png", settings.tankSpeed)
        self.gridPosition = [position_x // 200, position_y // 300]

    def shoot(self, bullets_array):
        # Creates and initialize bullet object with position 0,0 to get appropriate dimensions to shoot direction later
        new_bullet = TankBullet(0, 0, self.screen, self.current_image_angle)
        bullet_x, bullet_y = self.calculate_bullet_position(new_bullet)
        new_bullet.position["x"], new_bullet.position["y"] = bullet_x, bullet_y
        # bullets_array.append(new_bullet)
        bullets_array.add(new_bullet)

    def calculate_bullet_position(self, bullet):
        # places bullet in correct position to appear near to tank barrel
        if self.current_image_angle == 0:
            return self.position["x"] + (self.width / 2) - (bullet.width / 2), \
                   self.position["y"] - bullet.height
        elif self.current_image_angle == 90:
            return self.position["x"] - bullet.width, \
                   self.position["y"] + (self.height / 2) - (bullet.height / 2)
        elif self.current_image_angle == 180:
            return self.position["x"] + (self.width / 2) - (bullet.width / 2), \
                   self.position["y"] + self.height
        elif self.current_image_angle == 270:
            return self.position["x"] + self.width, \
                   self.position["y"] + (self.height / 2) - (bullet.height / 2)

    def explode(self, animation_objects):
        self.die()
        new_gif = GifAnimation("tank_explosion", 0, 6, self.position["x"] - 15,
                               self.position["y"] - 60, self.screen,
                               100)
        new_gif.load_frames()
        animation_objects.append(new_gif)

    def stop(self, direction):
        if direction == "UP":
            self.speed_y = 0
        if direction == "DOWN":
            self.speed_y = 0
        if direction == "LEFT":
            self.speed_x = 0
        if direction == "RIGHT":
            self.speed_x = 0

    def update(self, tanks_array, *args):
        Sprite.update(self)
        self.gridPosition = [self.position["x"] // 200, self.position["y"] // 300]





