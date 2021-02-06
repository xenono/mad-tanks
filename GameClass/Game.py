import pygame, random, time
from TankSubclasses.Player import Player
from TankSubclasses.Enemy import Enemy
from SpriteSubclasses.TankBullet import TankBullet
from GifAnimation.GifAnimation import GifAnimation
from settings import Settings

settings = Settings()


class Game:
    def __init__(self, screen):
        # All Sprites which are in game alive.
        self.tanksArray = []
        self.animationObjects = []
        self.bulletsArray = []
        self.screen = screen

        # Initializes objects for game
        self.playersTank = Player(settings.playerStartingPostition["x"], settings.playerStartingPostition["y"], screen)

        # Sets up interval to create Enemy every certain amount of time
        self.startTime = time.time()

        # Adds enemies
        for i in range(1):
            position_x = random.randint(70, 1350)
            position_y = random.randint(70, 840)
            enemy_tank = Enemy(position_x, position_y, screen, self.bulletsArray)
            self.tanksArray.append(enemy_tank)
            enemy_tank.make_decision(False)

        # Adds sprites to lists of certain type of sprite
        self.tanksArray.append(self.playersTank)

    def draw(self):
        # Draws every sprite which is in game
        for tank in self.tanksArray:
            tank.draw()
        for bullet in self.bulletsArray:
            bullet.draw()

    def handle_events(self):
        for event in pygame.event.get():
            # Closes the window when pressing X on upper taskbar
            if event.type == pygame.QUIT:
                running = False
                for tank in self.tanksArray:
                    tank.die()
                for bullet in self.bulletsArray:
                    bullet.die()
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.playersTank.move("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.playersTank.move("RIGHT")
                elif event.key == pygame.K_DOWN:
                    self.playersTank.move("DOWN")
                elif event.key == pygame.K_UP:
                    self.playersTank.move("UP")
                elif event.key == pygame.K_SPACE:
                    self.playersTank.shoot(self.bulletsArray)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.playersTank.stop("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.playersTank.stop("RIGHT")
                elif event.key == pygame.K_DOWN:
                    self.playersTank.stop("DOWN")
                elif event.key == pygame.K_UP:
                    self.playersTank.stop("UP")

    def create_new_enemy(self):
        current_time = time.time()
        if current_time - self.startTime > 1:
            start_time = time.time()
            position_x = random.randint(70, 1350)
            position_y = random.randint(70, 840)
            enemy_tank = Enemy(position_x, position_y, self.screen, self.bulletsArray)
            self.tanksArray.append(enemy_tank)
            enemy_tank.make_decision(False)

    def update(self):
        # prevents every sprite from leaving game surface borders
        for tank in self.tanksArray:
            if tank.position["x"] <= settings.borderSize:
                tank.position["x"] = settings.borderSize
            if tank.position["x"] + tank.width >= settings.screenWidth - settings.borderSize:
                tank.position["x"] = settings.screenWidth - tank.width - settings.borderSize
            if tank.position["y"] <= settings.borderSize:
                tank.position["y"] = settings.borderSize
            if tank.position["y"] + tank.height >= settings.screenHeight - settings.borderSize:
                tank.position["y"] = settings.screenHeight - tank.height - settings.borderSize

        # Updates sprites and screen
        for tank in self.tanksArray:
            if tank.alive:
                tank.update()
            else:
                tank.explode(self.animationObjects)
                self.tanksArray.remove(tank)
        # Updates bullets position and checks for any collisions with them.
        for bullet in self.bulletsArray:
            bullet.update()
            if not bullet.alive:
                bullet.explode(self.animationObjects)
                self.bulletsArray.remove(bullet)
            else:
                # Checks whether any alive bullet hit any tank
                for tank in self.tanksArray:
                    # Checks position of bullet and particular tank to verify hit
                    hit_spotted = bullet.check_for_hit(tank.width, tank.height, tank.position)
                    if hit_spotted:
                        # After hitting object bullet explodes and object is destroyed or loses one live point
                        bullet.alive = False
                        self.tanksArray.remove(tank)
                        tank.explode(self.animationObjects)
        # Checks and plays animations in appropriate moments.
        for animation in self.animationObjects:
            animation.update()
            if animation.is_finished:
                self.animationObjects.remove(animation)
