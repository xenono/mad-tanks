import pygame, random, time
from TankSubclasses.Player import Player
from TankSubclasses.Enemy import Enemy
from SpriteSubclasses.TankBullet import TankBullet
from GifAnimation.GifAnimation import GifAnimation
from settings import Settings
from GameClass.Game import Game

# Pygame setup
pygame.init()
pygame.font.init()
settings = Settings()
screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
# Game bar setup
pygame.display.set_caption("Tanks")
gameBackground = pygame.image.load("assets/background.jpg").convert()
menuBackground = pygame.image.load("assets/t-34Background.jpg").convert_alpha()
icon = pygame.image.load("assets/T-34.png").convert()
pygame.display.set_icon(icon)

gameObject = Game(screen)

# Game Status
running = True

clock = pygame.time.Clock()
while running:
    if gameObject.get_game_screen() == "Game":
        screen.blit(gameBackground, (0, 0))
        gameObject.draw_game()
        gameObject.handle_game_events()
        gameObject.update_game()

    elif gameObject.get_game_screen() == "Menu":
        screen.blit(menuBackground, (0, 0))
        gameObject.draw_menu()
        gameObject.handle_menu_events()
        gameObject.update_menu()

    elif gameObject.get_game_screen() == "Scorebo   ard":
        screen.blit(menuBackground, (0, 0))
        gameObject.draw_scoreboard()
        gameObject.handle_scoreboard_events()
        gameObject.update_scoreboard()

    elif gameObject.get_game_screen() == "Controls":
        screen.blit(menuBackground, (0, 0))
        gameObject.draw_controls()
        gameObject.handle_scoreboard_events()
        gameObject.update_controls()

    clock.tick(120)
    pygame.display.update()

pygame.quit()
quit()
