from SpriteSubclasses.Tank import Tank


class Player(Tank):
    def __init__(self, position_x, position_y, screen):
        super().__init__(position_x, position_y, screen)
        self.__score = 0

