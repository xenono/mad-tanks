import threading, random
from SpriteSubclasses.Tank import Tank


class Enemy(Tank):
    def __init__(self, position_x, position_y, screen, bullets_array):
        super().__init__(position_x, position_y, screen)
        self.__decision_delay = 0
        self.__bullets_array = bullets_array

    def make_decision(self):
        # Tank makes move every interval passed to threading.Timer
        threading.Timer(1.75, self.make_decision).start()
        # Randomly picks direction for Tank
        direction = random.choice(list(self.speed_and_direction.keys()))
        self.shoot(self.__bullets_array)

    def update(self):
        super(Enemy, self).update()
