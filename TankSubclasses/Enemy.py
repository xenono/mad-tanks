import random, time
from SpriteSubclasses.Tank import Tank
from TankSubclasses.Player import Player
from settings import Settings
import pygame

settings = Settings()


class Enemy(Tank):
    def __init__(self, position_x, position_y, screen, bullets_array):
        super().__init__(position_x, position_y, screen)

        self.image = pygame.image.load("assets/square_enemy.png").convert_alpha()

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

    def make_decision(self, is_on_border, players_grid):
        # pass

        if not self.alive:
            return

        if is_on_border:
            direction = random.choice(
                [direction for direction in self.possibleDirections if self.possibleDirections[direction]])
            self.move(direction)
            return

        current_time = time.time()
        if current_time - self.movingTimer > self.movingInterval:
            # Randomly picks direction for Tank
            direction = random.choice(
                [direction for direction in self.possibleDirections if self.possibleDirections[direction]])
            self.move(direction)
            self.movingTimer = time.time()
            self.movingInterval = random.randint(1, 3)

        current_time = time.time()
        if current_time - self.shootingTimer > self.shootingInterval:
            # self.shoot(self.bullets_array)
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

    def update(self, tanks_array, players_grid):
        Tank.update(self, tanks_array)

        # Triggers make_decision when object collides with walls
        if self.position["x"] >= settings.screenWidth - settings.borderSize - self.width:
            self.possibleDirections["RIGHT"] = False
            self.make_decision(True, players_grid)

        elif self.position["x"] <= settings.borderSize:
            self.possibleDirections["LEFT"] = False
            self.make_decision(True, players_grid)

        elif self.position["y"] >= settings.screenHeight - settings.borderSize - self.height:
            self.possibleDirections["DOWN"] = False
            self.make_decision(True, players_grid)

        elif self.position["y"] <= settings.borderSize:
            self.possibleDirections["UP"] = False
            self.make_decision(True, players_grid)

        else:
            self.possibleDirections = self.possibleDirections.fromkeys(self.possibleDirections, True)

        self.make_decision(False, players_grid)
