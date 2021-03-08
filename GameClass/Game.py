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
        self.tanksArray = pygame.sprite.Group()
        self.animationObjects = []
        self.bulletsArray = pygame.sprite.Group()
        self.screen = screen

        # Initializes objects for game
        # self.playersTank = Player(settings.playerStartingPostition["x"], settings.playerStartingPostition["y"], screen)
        self.playersTank = Player(1000, 300, screen)
        self.playersGrid = self.playersTank.gridPosition

        # Sets up interval to create Enemy every certain amount of time
        self.startTime = time.time()

        # Adds enemies
        for i in range(4):
            position_x = random.randint(70, 1350)
            # position_x = 700
            position_y = random.randint(70, 840)
            # position_y = 400
            enemy_tank = Enemy(position_x, position_y, screen, self.bulletsArray)
            # self.tanksArray.append(enemy_tank)
            self.tanksArray.add(enemy_tank)
            enemy_tank.make_decision(False, self.playersGrid)

        # Adds sprites to lists of certain type of sprite
        # self.tanksArray.append(self.playersTank)
        self.tanksArray.add(self.playersTank)

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
            # self.tanksArray.append(enemy_tank)
            self.tanksArray.add(enemy_tank)
            enemy_tank.make_decision(False, self.playersGrid)

    def update(self):
        # prevents every sprite from leaving game surface borders
        for tank_1 in self.tanksArray:
            if tank_1.position["x"] <= settings.borderSize:
                tank_1.position["x"] = settings.borderSize
            if tank_1.position["x"] + tank_1.width >= settings.screenWidth - settings.borderSize:
                tank_1.position["x"] = settings.screenWidth - tank_1.width - settings.borderSize
            if tank_1.position["y"] <= settings.borderSize:
                tank_1.position["y"] = settings.borderSize
            if tank_1.position["y"] + tank_1.height >= settings.screenHeight - settings.borderSize:
                tank_1.position["y"] = settings.screenHeight - tank_1.height - settings.borderSize

            # for tank_2 in self.tanksArray:
            #     if tank_2 == tank_1:
            #         continue
            #     if pygame.sprite.collide_rect(tank_1, tank_2):
            #         tank_1.speed_x = 0
            #         tank_1.speed_y = 0
            #         if tank_1.current_image_angle == 90:
            #             tank_1.position['x'] = tank_2.position['x'] + tank_2.width + 0.5
            #         if tank_1.current_image_angle == 270:
            #             tank_1.position['x'] = tank_2.position['x'] - 0.5
            #
            #         if tank_1.current_image_angle == 0:
            #             tank_1.position['y'] = tank_2.position['y'] + tank_2.height + 0.5
            #         if tank_1.current_image_angle == 180:
            #             tank_1.position['y'] = tank_2.position['y'] - 0.5

        # Updates sprites and screen
        for tank in self.tanksArray:
            if tank != self.playersTank:
                # if self.playersTank.speed_x == tank.speed_x and self.playersTank.speed_y == tank.speed_y:
                #     print(self)
                if self.playersTank.position['x'] + self.playersTank.width > tank.position['x'] and self.playersTank.position['x'] < tank.position['x']  + tank.width:
                    if (tank.position['y'] < self.playersTank.position['y'] < tank.position['y'] + tank.height) or (
                            tank.position['y'] < self.playersTank.position['y'] + self.playersTank.height < tank.position['y'] + tank.height):
                        if self.playersTank.current_image_angle == 0:
                            self.playersTank.position['y'] = tank.height + tank.position['y']
                        elif self.playersTank.current_image_angle == 180:
                            self.playersTank.position['y'] = tank.position['y'] - self.playersTank.height
                        elif self.playersTank.current_image_angle == 270:
                            self.playersTank.position['x'] = tank.position['x'] - self.playersTank.width
                        elif self.playersTank.current_image_angle == 90:
                            self.playersTank.position['x'] = tank.position['x'] + tank.width
            if tank.alive:
                if isinstance(tank,Enemy):
                    tank.update(self.tanksArray, self.playersGrid)
                else:
                    tank.update(self.tanksArray)
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

        self.playersGrid = self.playersTank.gridPosition

