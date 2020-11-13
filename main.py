import pygame
from objects.players_tank import PlayersTank

pygame.init()

screenX = 1000
screenY = 600
borderSize = 5
screen = pygame.display.set_mode((screenX, screenY))


pygame.display.set_caption("Tanks")
background = pygame.image.load("assets/background.jpg").convert_alpha()

playersTank = PlayersTank(500, 300, screen)

# All objects which are in game alive.
inGameObjects = [playersTank]


running = True
while running:

    screen.blit(background, (0, 0))
    playersTank.draw()

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

    for sprite in inGameObjects:
        if sprite.position["x"] <= borderSize:
            sprite.position["x"] = borderSize
        if sprite.position["x"] + sprite.width >= screenX - borderSize:
            sprite.position["x"] = screenX - sprite.width - borderSize
        if sprite.position["y"] <= borderSize:
            sprite.position["y"] = borderSize
        if sprite.position["y"] + sprite.height >= screenY - borderSize:
            sprite.position["y"] = screenY - sprite.height - borderSize





    playersTank.update()
    pygame.display.update()
