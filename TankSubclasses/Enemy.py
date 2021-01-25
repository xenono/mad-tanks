import random, time
from SpriteSubclasses.Tank import Tank


class Enemy(Tank):
    def __init__(self, position_x, position_y, screen, bullets_array):
        super().__init__(position_x, position_y, screen)
        self.decision_delay = 0
        self.bullets_array = bullets_array
        # Start decision timer
        self.timer = time.time()
        # Break between making decisions
        self.interval = 0

    def make_decision(self):
        current_time = time.time()
        if not self.alive:
            return
        if current_time - self.timer < self.interval:
            return
        # Randomly picks direction for Tank
        direction = random.choice(list(self.speed_and_direction.keys()))
        self.shoot(self.bullets_array)
        self.move(direction)
        self.timer = time.time()
        self.interval = random.randint(1, 4)

    def update(self):
        super(Enemy, self).update()
        self.make_decision()
