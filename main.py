import pygame
from SpriteSubclasses.PlayersTank import PlayersTank
from SpriteSubclasses.EnemyTank import EnemyTank

# Pygame setup
pygame.init()
screenX = 1000
screenY = 600
borderSize = 5
screen = pygame.display.set_mode((screenX, screenY))
# Game bar setup
pygame.display.set_caption("Tanks")
background = pygame.image.load("assets/background.jpg").convert_alpha()
icon = pygame.image.load("assets/player_tank.png")
pygame.display.set_icon(icon)

# Adds player's tank object
playersTank = PlayersTank(500, 300, screen)
enemyTank = EnemyTank(100, 100, screen)
# enemyTank.make_decision()
#

# All SpriteSubclasses which are in game alive.
inGameObjects = [playersTank, enemyTank]

running = True
while running:

    screen.blit(background, (0, 0))
    playersTank.draw()
    # enemyTank.draw()

    for event in pygame.event.get():
        # Closes the window when pressing X on upper taskbar
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playersTank.move("LEFT")
            elif event.key == pygame.K_RIGHT:
                playersTank.move("RIGHT")
            elif event.key == pygame.K_DOWN:
                playersTank.move("DOWN")
            elif event.key == pygame.K_UP:
                playersTank.move("UP")

        if event.type == pygame.KEYUP:
            playersTank.stop()

    # prevents every sprite to leave game surface borders
    for sprite in inGameObjects:
        if sprite.position["x"] <= borderSize:
            sprite.position["x"] = borderSize
        if sprite.position["x"] + sprite.width >= screenX - borderSize:
            sprite.position["x"] = screenX - sprite.width - borderSize
        if sprite.position["y"] <= borderSize:
            sprite.position["y"] = borderSize
        if sprite.position["y"] + sprite.height >= screenY - borderSize:
            sprite.position["y"] = screenY - sprite.height - borderSize

    # Updates sprites and screen
    playersTank.update()
    # enemyTank.update()
    pygame.display.update()
