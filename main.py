import pygame
from TankSubclasses.Player import Player
from TankSubclasses.Enemy import Enemy
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

# All Sprites which are in game alive.
tanksArray = []
animationObjects = []
bulletsArray = []

# Initializes objects for game
enemyTank = Enemy(400, 300, screen, bulletsArray)
playersTank = Player(500, 300, screen)

# Adds sprites to lists of certain type of sprite
tanksArray.append(playersTank)
tanksArray.append(enemyTank)
enemyTank.make_decision()

running = True
while running:

    screen.blit(background, (0, 0))

    # Draws every sprite which is in game
    for tank in tanksArray:
        tank.draw()
    for bullet in bulletsArray:
        bullet.draw()

    for event in pygame.event.get():
        # Closes the window when pressing X on upper taskbar
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break

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
                playersTank.shoot(bulletsArray)

        if event.type == pygame.KEYUP:
            playersTank.stop()

    # Stops program just after X is clicked
    if not running:
        break

    # prevents every sprite from leaving game surface borders
    for tank in tanksArray:
        if tank.position["x"] <= borderSize:
            tank.position["x"] = borderSize
        if tank.position["x"] + tank.width >= screenX - borderSize:
            tank.position["x"] = screenX - tank.width - borderSize
        if tank.position["y"] <= borderSize:
            tank.position["y"] = borderSize
        if tank.position["y"] + tank.height >= screenY - borderSize:
            tank.position["y"] = screenY - tank.height - borderSize

    # Updates sprites and screen
    for tank in tanksArray:
        tank.update()
        if not tank.alive:
            tank.explode(animationObjects)
            tanksArray.remove(tank)
    # Updates bullets position and checks for any collisions with them.
    for bullet in bulletsArray:
        bullet.update()
        if not bullet.alive:
            bullet.explode(animationObjects)
            bulletsArray.remove(bullet)
        else:
            # Checks whether any alive bullet hit any tank
            for tank in tanksArray:
                # Checks position of bullet and particular tank to verify hit
                hitSpotted = bullet.check_for_hit(tank.width, tank.height, tank.position)
                if hitSpotted:
                    # After hitting object bullet explodes and object is destroyed or loses one live point
                    bullet.alive = False
                    tanksArray.remove(tank)
                    tank.explode(animationObjects)
    # Checks and plays animations in appropriate moments.
    for animation in animationObjects:
        animation.update()
        if animation.is_finished:
            animationObjects.remove(animation)

    pygame.display.update()
