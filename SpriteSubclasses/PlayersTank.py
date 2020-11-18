import pygame
from Sprite.Sprite import Sprite
from SpriteSubclasses.TankBullet import TankBullet


class PlayersTank(Sprite):
    def __init__(self, position_x, position_y, screen):
        super().__init__(screen, 50, 76, position_x, position_y, "assets/player_tank.png")

    def shoot(self, in_game_objects):
        new_bullet = TankBullet(100, 100, self.screen, self.current_image_angle)
        bullet_x, bullet_y = self.calculate_bullet_position(new_bullet)
        new_bullet.position["x"], new_bullet.position["y"] = bullet_x, bullet_y
        in_game_objects.append(new_bullet)

    def calculate_bullet_position(self, bullet):
        if self.current_image_angle == 0:
            return self.position["x"] + (self.width / 2) - bullet.width, \
                   self.position["y"] - bullet.height / 2
        elif self.current_image_angle == 90:
            return self.position["x"] - bullet.width, \
                   self.position["y"] + bullet.height / 2
        elif self.current_image_angle == 180:
            return self.position["x"] + (self.width / 2) - bullet.width, \
                   self.position["y"] - bullet.height / 2 - 5
        elif self.current_image_angle == 270:
            return self.position["x"] + (self.width / 2) - bullet.width, \
                   self.position["y"] - bullet.height / 2 - 5





