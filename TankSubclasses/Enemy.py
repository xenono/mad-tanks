import random, time
from SpriteSubclasses.Tank import Tank
from TankSubclasses.Player import Player
from settings import Settings
import pygame

settings = Settings()


class Enemy(Tank):
    def __init__(self, position_x, position_y, screen, bullets_array, tank_type):
        super().__init__(position_x, position_y, screen)

        self.image = pygame.image.load("assets/{}.png".format(tank_type)).convert_alpha()
        if tank_type == "panzer_4":
            self.health = 1
        elif tank_type == "panther":
            self.health = 2
        elif tank_type == "Tiger":
            self.health = 3
        self.decision_delay = 0
        self.bullets_array = bullets_array
        # Start decision timer
        self.movingTimer = time.time()
        self.shootingTimer = time.time()
        self.attack_timer = time.time()
        # Break between making decisions
        self.movingInterval = 0
        self.shootingInterval = 0
        # Tells if enemy is moving
        self.isMoving = False
        self.possibleDirections = {"UP": True, "DOWN": True, "LEFT": True, "RIGHT": True}

    def make_decision(self, is_on_object):
        # pass
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

    def choose_path_randomly(self):
        try:
            direction = random.choice(
                [direction for direction in self.possibleDirections if self.possibleDirections[direction]])
            self.move(direction)
        except IndexError:
            self.speed_x = 0
            self.speed_y = 0
            self.die()

    def attack_direction(self, direction):
        self.move(direction)
        self.shoot(self.bullets_array)
        self.make_decision(True)

    def player_in_range(self, player):
        player_x = player.position["x"]
        player_y = player.position["y"]
        current_time = time.time()
        if not current_time - self.attack_timer >= 2.75:
            return
        # Checks each side to attack player if he is closer than 250 pixels away
        # Right and Left side
        if self.position["y"] + self.height - 25 >= player_y >= self.position["y"] - 20:
            if player_x - self.position["x"] - self.width <= settings.screenWidth and \
                    player_x + player.width > self.position["x"] + self.width:
                self.attack_direction("RIGHT")
                self.attack_timer = time.time()
            elif self.position["x"] - player_x - player.width <= settings.screenWidth and \
                    self.position["x"] > player_x + player.width:
                self.attack_direction("LEFT")
                self.attack_timer = time.time()
        # Checks Upper and down side
        elif self.position["x"] + 5 <= player_x <= self.position["x"] + self.width - 5 or \
                self.position["x"] + 5 <= player_x + player.width <= self.position["x"] + self.width - 5:
            # Upper side
            if self.position["y"] - player_y - player.height <= settings.screenHeight and \
                    self.position["y"] > player_y + player.height:
                self.attack_direction("UP")
                self.attack_timer = time.time()
            # Down side
            elif player_y - self.position["y"] - self.height <= settings.screenHeight and \
                    player_y + player.height > self.position["y"] + self.height:
                self.attack_direction("DOWN")
                self.attack_timer = time.time()

    def update(self, tanks_array, player):
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

        # Collision with other tanks and buildings
        for tank in tanks_array:
            if tank != self:
                if self.position['x'] + self.width >= tank.position['x'] and \
                        self.position['x'] <= tank.position['x'] + tank.width:
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
                        elif self.current_image_angle == 90:
                            self.speed_x = 0
                            self.possibleDirections["LEFT"] = False
                            self.make_decision(True)
                            return

        # Checks if player is in range to attack
        self.player_in_range(player)

        self.make_decision(False)
