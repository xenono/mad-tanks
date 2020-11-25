import pygame
from SpriteSubclasses.PlayersTank import PlayersTank
from SpriteSubclasses.EnemyTank import EnemyTank
from SpriteSubclasses.TankBullet import TankBullet
from GifAnimation.GifAnimation import GifAnimation

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
# Adds enemy's tank object
# enemyTank = EnemyTank(100, 100, screen)
# enemyTank.make_decision()

# All SpriteSubclasses which are in game alive.
inGameObjects = []
animationObjects = []

playersTank = PlayersTank(500, 300, screen)
inGameObjects.append(playersTank)

running = True
while running:

    screen.blit(background, (0, 0))

    # Draws every sprite which is in game
    for sprite in inGameObjects:
        sprite.draw()

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
            elif event.key == pygame.K_SPACE:
                playersTank.shoot(inGameObjects)

        if event.type == pygame.KEYUP:
            playersTank.stop()

    # prevents every sprite from leaving game surface borders
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
    for sprite in inGameObjects:
        sprite.update()
        if not sprite.alive:
            sprite.explode(animationObjects)
            inGameObjects.remove(sprite)
    for animation in animationObjects:
        animation.update()
        if animation.is_finished:
            animationObjects.remove(animation)

    pygame.display.update()
