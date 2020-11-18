from Sprite.Sprite import Sprite

# Constant possible direction of movement direction : angle
DIRECTIONS = {
    "UP": 0,
    "LEFT": 90,
    "DOWN": 180,
    "RIGHT": 270
}


class TankBullet(Sprite):
    def __init__(self, position_x, position_y, screen, tank_angle):
        super().__init__(screen, 5, 45, position_x, position_y, "assets/bullet_10.png")
        for direction, angle in DIRECTIONS.items():
            if angle == tank_angle:
                self.direction = direction

        if self.direction == "LEFT" or self.direction == "RIGHT":
            self.width, self.height = self.height, self.width

        self.move(self.direction)
