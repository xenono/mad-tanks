import pygame, random, time, os, json
from TankSubclasses.Player import Player
from TankSubclasses.Enemy import Enemy
from SpriteSubclasses.TankBullet import TankBullet
from GifAnimation.GifAnimation import GifAnimation
from StaticSprite.StaticSprite import StaticSprite
from utils.CollisionDetection import CollisionDetection
from settings import Settings

settings = Settings()


class Game:
    def __init__(self, screen):
        # All Sprites which are in game alive.
        self.tanksArray = []
        self.animationObjects = []
        self.bulletsArray = []
        self.buildingsArray = []
        self.screen = screen

        # All animations frames
        self. animations = {
            "bulletExplosion": GifAnimation.load_frames(24, 0, "explosion_50"),
            "tankExplosion": GifAnimation.load_frames(0, 6, "tank_explosion"),
        }

        # Initializes objects for game
        self.playersTank = Player(1000, 300, screen)

        # Sets up interval to create Enemy every certain amount of time
        self.startTime = time.time()

        # Creates levels from level json file
        base_path = os.path.abspath(os.getcwd())
        for file_name in os.listdir(os.path.join(base_path, "levels")):
            file_path = os.path.join(base_path, "levels", file_name)
            with open(file_path) as file:
                data = json.load(file)

                # # Adds buildings
                for building in data['buildings']:
                    building_object = StaticSprite(screen, building["x"], building["y"],
                                                   "assets/" + building["type"] + ".png")
                    self.buildingsArray.append(building_object)

                # Adds enemies
                for tank_data in data['enemies']:
                    position_x = tank_data["x"]
                    position_y = tank_data["y"]
                    enemy_tank = Enemy(position_x, position_y, screen, self.bulletsArray)
                    self.tanksArray.append(enemy_tank)

        # Adds sprites to lists of certain type of sprite
        self.tanksArray.append(self.playersTank)

    def draw(self):
        # Draws every sprite which is in game
        for tank in self.tanksArray:
            tank.draw()
        for bullet in self.bulletsArray:
            bullet.draw()
        for building in self.buildingsArray:
            building.draw()

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
                    if self.playersTank.canShoot:
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
            self.tanksArray.append(enemy_tank)
            enemy_tank.make_decision(False)

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

        # Updates sprites and screen
        for tank in self.tanksArray:
            if tank.alive:
                if isinstance(tank, Enemy):
                    tank.update(self.tanksArray, self.playersTank)
                else:
                    tank.update(self.tanksArray)
            else:
                tank.explode(self.animations["tankExplosion"], self.animationObjects)
                self.tanksArray.remove(tank)

        # Updates bullets position and checks for any collisions with them.
        for bullet in self.bulletsArray:
            bullet.update()
            if not bullet.alive:
                bullet.explode(self.animations["bulletExplosion"], self.animationObjects)
                self.bulletsArray.remove(bullet)
            else:
                # Checks whether any alive bullet hit any tank
                for tank in self.tanksArray:
                    if isinstance(tank, Enemy) and isinstance(bullet.shooter, Enemy):
                        continue
                    # Checks position of bullet and particular tank to verify hit
                    hit_spotted = bullet.check_for_hit(tank.width, tank.height, tank.position)
                    if hit_spotted:
                        # After hitting object bullet explodes and object is destroyed or loses one live point
                        bullet.alive = False
                        tank.get_shot()
                        if tank.health == 0:
                            self.tanksArray.remove(tank)
                            tank.explode(self.animations["tankExplosion"], self.animationObjects)
                for building in self.buildingsArray:
                    hit_spotted = CollisionDetection.collision(bullet, building)
                    if hit_spotted:
                        bullet.alive = False

        # Checks for tank collisions with building
        for tank in self.tanksArray:
            for building in self.buildingsArray:
                if CollisionDetection.collision(tank, building):
                    CollisionDetection.position_tank_relatively_to_moving_direction(tank, building)
                    if isinstance(tank, Enemy):
                        tank.make_decision(True)

        # Checks and plays animations in appropriate moments.
        for animation in self.animationObjects:
            animation.update()
            if animation.is_finished:
                self.animationObjects.remove(animation)

        for building in self.buildingsArray:
            building.update()
