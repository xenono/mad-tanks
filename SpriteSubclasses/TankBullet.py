from Sprite.Sprite import  Sprite


class TankBullet(Sprite):
    def __init__(self,  screen, position_x, position_y):
        super().__init__(screen, 50, 76, position_x, position_y, "assets/player_tank.png")