import pygame
from Sprite.Sprite import Sprite


class PlayersTank(Sprite):
    def __init__(self, position_x, position_y, screen):
        super().__init__(screen, 50, 76, position_x, position_y, "assets/player_tank.png")




