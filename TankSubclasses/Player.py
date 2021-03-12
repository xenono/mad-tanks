from SpriteSubclasses.Tank import Tank
from settings import Settings
from utils.CollisionDetection import CollisionDetection

import pygame, time

settings = Settings()


class Player(Tank):
    def __init__(self, position_x, position_y, screen):
        super().__init__(position_x, position_y, screen)
        self.health = settings.playersHealthNumber
        self.score = 0
        self.shotCoolDown = settings.playersShootCooldown
        self.shotCoolDownTimeCounter = time.time()
        self.canShoot = True

    def shoot(self, bullets_array):
        super(Player, self).shoot(bullets_array)
        self.canShoot = False
        self.shotCoolDownTimeCounter = time.time()

    def update(self, tanks_array):
        Tank.update(self, tanks_array)

        current_time = time.time()

        if self.canShoot is False and current_time - self.shotCoolDownTimeCounter > self.shotCoolDown:
            self.shotCoolDownTimeCounter = time.time()
            self.canShoot = True

        for tank in tanks_array:
            if tank != self:
                if CollisionDetection.collision(self,tank):
                    CollisionDetection.position_tank_relatively_to_moving_direction(self, tank)
