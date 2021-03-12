import random, time
from SpriteSubclasses.Tank import Tank
from TankSubclasses.Player import Player
from settings import Settings
import pygame

settings = Settings()


class Enemy(Tank):
    def __init__(self, position_x, position_y, screen, bullets_array):
        super().__init__(position_x, position_y, screen)

        self.image = pygame.image.load("assets/Tiger.png").convert_alpha()

        self.decision_delay = 0
        self.bullets_array = bullets_array
        # Start decision timer
        self.movingTimer = time.time()
        self.shootingTimer = time.time()
        # Break between making decisions
        self.movingInterval = 0
        self.shootingInterval = 0
        # Tells if enemy is moving
        self.isMoving = False
        self.possibleDirections = {"UP": True, "DOWN": True, "LEFT": True, "RIGHT": True}

    def make_decision(self, is_on_object):
        if not self.alive:
            return

        if is_on_object:
            self.choose_path_randomly()
            return

        current_time = time.time()
        if current_time - self.movingTimer > self.movingInterval:
            # Randomly picks direction for Tank
            self.choose_path_randomly()
            self.movingTimer = time.time()
            self.movingInterval = random.randint(1, 3)

        current_time = time.time()
        if current_time - self.shootingTimer > self.shootingInterval:
            self.shoot(self.bullets_array)
            self.shootingTimer = time.time()
            self.shootingInterval = random.randint(1, 3)

    @staticmethod
    def lower_the_difference(num_1, num_2):
        # num_1 wants to be num_2
        if num_2 > num_1:
            return num_1 + 1
        elif num_2 < num_1:
            return num_1 - 1
        else:
            return num_1

    def choose_path_randomly(self):
        try:
            direction = random.choice(
                [direction for direction in self.possibleDirections if self.possibleDirections[direction]])
            self.move(direction)
        except IndexError:
            self.speed_x = 0
            self.speed_y = 0
            self.die()

    def update(self, tanks_array, players_grid):
        Tank.update(self, tanks_array)

        # Triggers make_decision when object collides with walls
        if self.position["x"] >= settings.screenWidth - settings.borderSize - self.width:
            self.possibleDirections["RIGHT"] = False
            self.make_decision(True)

        elif self.position["x"] <= settings.borderSize:
            self.possibleDirections["LEFT"] = False
            self.make_decision(True)

        elif self.position["y"] >= settings.screenHeight - settings.borderSize - self.height:
            self.possibleDirections["DOWN"] = False
            self.make_decision(True)

        elif self.position["y"] <= settings.borderSize:
            self.possibleDirections["UP"] = False
            self.make_decision(True)
        else:
            self.possibleDirections = self.possibleDirections.fromkeys(self.possibleDirections, True)

        for tank in tanks_array:
            if tank != self:
                if self.position['x'] + self.width >= tank.position['x'] and self.position['x'] <= tank.position[
                    'x'] + tank.width:
                    if (tank.position['y'] <= self.position['y'] < tank.position['y'] + tank.height) or (
                            tank.position['y'] <= self.position['y'] + self.height < tank.position['y'] + tank.height):
                        if self.current_image_angle == 0:
                            # self.position['y'] = tank.height + tank.position['y']
                            self.speed_y = 0
                            self.possibleDirections["UP"] = False
                            self.make_decision(True)
                            return
                        elif self.current_image_angle == 180:
                            # self.position['y'] = tank.position['y'] - self.height
                            self.speed_y = 0
                            self.possibleDirections["DOWN"] = False
                            self.make_decision(True)
                            return
                        elif self.current_image_angle == 270:
                            self.speed_x = 0
                            self.possibleDirections["RIGHT"] = False
                            self.make_decision(True)
                            return
                            # self.position['x'] = tank.position['x'] - self.width
                        elif self.current_image_angle == 90:
                            # self.position['x'] = tank.position['x'] + tank.width
                            self.speed_x = 0
                            self.possibleDirections["LEFT"] = False
                            self.make_decision(True)
                            return

        self.make_decision(False)
