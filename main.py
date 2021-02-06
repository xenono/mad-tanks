import pygame, random, time
from TankSubclasses.Player import Player
from TankSubclasses.Enemy import Enemy
from SpriteSubclasses.TankBullet import TankBullet
from GifAnimation.GifAnimation import GifAnimation
from settings import Settings
from GameClass.Game import Game

# Pygame setup
pygame.init()
settings = Settings()
screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
# Game bar setup
pygame.display.set_caption("Tanks")
background = pygame.image.load("assets/background.jpg").convert()
icon = pygame.image.load("assets/player_tank.png").convert()
pygame.display.set_icon(icon)

gameObject = Game(screen)

# Game Status
running = True

while running:
    screen.blit(background, (0, 0))

    gameObject.draw()
    gameObject.handle_events()

    gameObject.update()

    pygame.display.update()

pygame.quit()
quit()
