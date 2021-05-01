import pygame, random, time, os, json
from TankSubclasses.Player import Player
from TankSubclasses.Enemy import Enemy
from SpriteSubclasses.TankBullet import TankBullet
from GifAnimation.GifAnimation import GifAnimation
from StaticSprite.StaticSprite import StaticSprite
from Button.Button import Button
from Mouse.Mouse import Mouse
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
        self._gameScreen = "Menu"
        self.mouse = Mouse()
        self.menu_title = pygame.image.load("assets/menuTitle.png")
        self.menu_play_button = Button(self.screen, 706, 87, "assets/playButton.png", "assets/activePlayButton.png",
                                       225, self.mouse)
        self.menu_exit_button = Button(self.screen, 706, 87, "assets/exitButton.png", "assets/activeExitButton.png",
                                       525, self.mouse)
        self.menu_controls_button = Button(self.screen, 706, 87, "assets/controlsButton.png",
                                           "assets/activeControlsButton.png",
                                           375, self.mouse)
        self.main_menu_button = Button(self.screen, 706, 87, "assets/mainMenuButton.png",
                                       "assets/activeMainMenuButton.png", 500, self.mouse)
        self.controlsBoard = pygame.image.load("assets/controlsBoard2.png")
        self.font = pygame.font.Font("fonts/Montserrat-Bold.ttf", 48)
        self.healthImage = pygame.image.load("assets/heart.png")

        # All animations frames
        self.animations = {
            "bulletExplosion": GifAnimation.load_frames(24, 0, "explosion_50"),
            "tankExplosion": GifAnimation.load_frames(0, 6, "tank_explosion"),
        }

        # Initializes objects for game
        self.playersTank = Player(1000, 300, screen)

        # Sets up interval to create Enemy every certain amount of time
        self.startTime = time.time()

    def reset_level(self):
        self.buildingsArray = []
        self.tanksArray = []
        self.animationObjects = []
        self.bulletsArray = []
        self.playersTank.health = 3
        self.playersTank.alive = True
        # Creates levels from level json file
        base_path = os.path.abspath(os.getcwd())
        for file_name in os.listdir(os.path.join(base_path, "levels")):
            file_path = os.path.join(base_path, "levels", file_name)
            with open(file_path) as file:
                data = json.load(file)

                # Adds buildings
                for building in data['buildings']:
                    building_object = StaticSprite(self.screen, building["x"], building["y"],
                                                   "assets/" + building["type"] + ".png")
                    self.buildingsArray.append(building_object)

                # Adds enemies
                for tank_data in data['enemies']:
                    position_x = tank_data["x"]
                    position_y = tank_data["y"]
                    tank_type = tank_data["type"]
                    enemy_tank = Enemy(position_x, position_y, self.screen, self.bulletsArray, tank_type)
                    self.tanksArray.append(enemy_tank)

        # Adds sprites to lists of certain type of sprite
        self.tanksArray.append(self.playersTank)

    def get_game_screen(self):
        return self._gameScreen

    def set_game_screen(self, screen):
        self._gameScreen = screen

    def draw_game(self):
        # Draws every sprite which is in game
        for tank in self.tanksArray:
            tank.draw()
        for bullet in self.bulletsArray:
            bullet.draw()
        for building in self.buildingsArray:
            building.draw()
        for i in range(self.playersTank.health):
            self.screen.blit(self.healthImage, (settings.screenWidth - 100 + (32 * i), settings.screenHeight - 40))

    def draw_menu(self):
        self.screen.blit(self.menu_title, (settings.screenWidth / 2 - 353, 50))
        self.menu_play_button.draw()
        self.menu_exit_button.draw()
        self.menu_controls_button.draw()

    def draw_scoreboard(self):
        self.screen.blit(self.menu_title, (settings.screenWidth / 2 - 353, 50))
        if self.playersTank.health == 0:
            text = self.font.render("Enemies destroyed you!", False, (255, 255, 255))
            self.screen.blit(text, (settings.screenWidth / 2 - text.get_width() / 2, 300))

        elif self.playersTank.health > 0 and len(self.tanksArray) == 1 and self.tanksArray[0] == self.playersTank:
            text_1 = self.font.render("Congratulations!", False, (255, 255, 255))
            text_2 = self.font.render("You have destroyed all your enemies.", False, (255, 255, 255))
            self.screen.blit(text_1, (settings.screenWidth / 2 - text_1.get_width() / 2, 275))
            self.screen.blit(text_2, (settings.screenWidth / 2 - text_2.get_width() / 2, 350))

        self.main_menu_button.draw()

    def draw_controls(self):
        self.screen.blit(self.menu_title, (settings.screenWidth / 2 - 353, 50))
        self.screen.blit(self.controlsBoard, (settings.screenWidth / 2 - 353, 200))
        self.main_menu_button.draw()

    def handle_menu_events(self):
        for event in pygame.event.get():
            # Closes the window when pressing X on upper taskbar
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CollisionDetection.collision(self.mouse, self.menu_play_button):
                    self.reset_level()
                    self.set_game_screen("Game")
                elif CollisionDetection.collision(self.mouse, self.menu_controls_button):
                    self.set_game_screen("Controls")
                elif CollisionDetection.collision(self.mouse, self.menu_exit_button):
                    pygame.quit()
                    quit()

    def handle_scoreboard_events(self):
        for event in pygame.event.get():
            # Closes the window when pressing X on upper taskbar
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CollisionDetection.collision(self.mouse, self.main_menu_button):
                    self.reset_level()
                    self.set_game_screen("Menu")

    def handle_game_events(self):
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

    def update_menu(self):
        self.menu_play_button.update()
        self.menu_exit_button.update()
        self.menu_controls_button.update()
        self.mouse.update()

    def update_scoreboard(self):
        self.main_menu_button.update()
        self.menu_exit_button.update()
        self.mouse.update()

    def update_controls(self):
        self.main_menu_button.update()
        self.mouse.update()

    def update_game(self):
        # Checks if player lost
        if self.playersTank.health == 0:
            self.set_game_screen("Scoreboard")
            return
        # Checks if player win
        if len(self.tanksArray) == 1 and self.tanksArray[0] == self.playersTank and len(self.animationObjects) == 0:
            self.set_game_screen("Scoreboard")
            return
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
