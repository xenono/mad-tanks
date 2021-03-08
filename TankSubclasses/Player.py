from SpriteSubclasses.Tank import Tank
import pygame


class Player(Tank):
    def __init__(self, position_x, position_y, screen):
        super().__init__(position_x, position_y, screen)
        self.score = 0

    def update(self, tanks_array):
        Tank.update(self, tanks_array)

        # for tank in tanks_array:
        #                 if tank != self:
        #         if self.speed_x == tank.speed_x and self.speed_y == tank.speed_y:
        #             print(self)
        #         if self.position['x'] + self.width > tank.position['x'] and self.position['x'] < tank.position['x']  + tank.width:
        #             if (tank.position['y'] < self.position['y'] < tank.position['y'] + tank.height) or (
        #                     tank.position['y'] < self.position['y'] + self.height < tank.position['y'] + tank.height):
        #                 if self.current_image_angle == 0:
        #                     self.position['y'] = tank.height + tank.position['y']
        #                 elif self.current_image_angle == 180:
        #                     self.position['y'] = tank.position['y'] - self.height
        #                 elif self.current_image_angle == 270:
        #                     self.position['x'] = tank.position['x'] - self.width
        #                 elif self.current_image_angle == 90:
        #                     self.position['x'] = tank.position['x'] + tank.width
