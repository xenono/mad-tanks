import random, time
from SpriteSubclasses.Tank import Tank
from settings import Settings

settings = Settings()


class Enemy(Tank):
    def __init__(self, position_x, position_y, screen, bullets_array):
        super().__init__(position_x, position_y, screen)
        self.decision_delay = 0
        self.bullets_array = bullets_array
        # Start decision timer
        self.timer = time.time()
        # Break between making decisions
        self.interval = 0
        # Tells if enemy is moving
        self.isMoving = False
        self.possibleDirections = {"UP": True, "DOWN": True, "LEFT": True, "RIGHT": True}

    def make_decision(self, is_on_border):
        current_time = time.time()
        if not self.alive:
            return
        if current_time - self.timer < self.interval and not is_on_border:
            return

        # Randomly picks direction for Tank
        direction = random.choice(
            [direction for direction in self.possibleDirections if self.possibleDirections[direction]])
        # self.shoot(self.bullets_array)
        self.move(direction)
        self.timer = time.time()
        self.interval = random.randint(1, 3)

    def update(self):
        super(Enemy, self).update()
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
        self.make_decision(False)
