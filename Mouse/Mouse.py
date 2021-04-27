import pygame


class Mouse:
    def __init__(self):
        self.width = 1
        self.height = 1
        x, y = pygame.mouse.get_pos()
        self.position = {
            "x": x,
            "y": y
        }

    def update(self):
        x, y = pygame.mouse.get_pos()

        self.position["x"] = x
        self.position["y"] = y
