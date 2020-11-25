import pygame
from Sprite.Sprite import Sprite
from GifAnimation.GifAnimation import GifAnimation


# Constant possible direction of movement direction : angle
DIRECTIONS = {
    "UP": 0,
    "LEFT": 90,
    "DOWN": 180,
    "RIGHT": 270
}


class TankBullet(Sprite):
    def __init__(self, position_x, position_y, screen, tank_angle):
        super().__init__(screen, 10, 30, position_x, position_y, "assets/bullet_10.png", 1.2)
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        for direction, angle in DIRECTIONS.items():
            if angle == tank_angle:
                self.direction = direction

        self.move(self.direction)
        self.exploded = False

    def update(self):
        super().update()
        self.check_for_border_hit()

    def check_for_border_hit(self):
        if self.position["x"] <= 5 or self.position["x"] + self.width >= self.window_width - 5.5:
            self.alive = False
        if self.position["y"] <= 5 or self.position["y"] + self.height >= self.window_height - 5.5:
            self.alive = False

    def explode(self, animation_objects):
        if not self.alive:
            new_gif = GifAnimation("explosion", 24, 0, self.position["x"], self.position["y"], self.screen)
            new_gif.load_frames()
            animation_objects.append(new_gif)


