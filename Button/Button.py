import pygame
from settings import Settings
from utils.CollisionDetection import CollisionDetection

settings = Settings()


class Button:
    def __init__(self, screen, width, height, basic_image, while_active_image, top_margin, mouse):
        self.screen = screen
        self.width = width
        self.height = height
        self.mouse = mouse
        self.top_margin = top_margin
        self.basic_image = pygame.image.load(basic_image)
        self.while_active_image = pygame.image.load(while_active_image)
        self.current_image = self.basic_image
        self.position = {
            "x": settings.screenWidth / 2 - 353,
            "y": self.top_margin
        }

    def draw(self):
        self.screen.blit(self.current_image, (settings.screenWidth / 2 - 353, self.top_margin))

    def update(self):
        if CollisionDetection.collision(self.mouse, self):
            self.current_image = self.while_active_image
        else:
            self.current_image = self.basic_image
