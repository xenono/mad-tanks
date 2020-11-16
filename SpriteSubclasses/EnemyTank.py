import threading
import random
from Sprite.Sprite import Sprite


class EnemyTank(Sprite):
    def __init__(self, position_x, position_y, screen):
        super().__init__(screen, 50, 76, position_x, position_y, "assets/player_tank.png")
        self.decision_delay = 0

    def make_decision(self):
        threading.Timer(1.75, self.make_decision).start()
        direction = random.choice(list(self.speed_and_direction.keys()))
        self.move(direction)

    def update(self):
        super(EnemyTank, self).update()
