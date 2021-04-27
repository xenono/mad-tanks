class Settings:
    """
        Class to store some global constants
    """

    def __init__(self):
        # Window settings
        self.screenWidth = 1300
        self.screenHeight = 700
        self.borderSize = 5

        # Tank settings
        self.tankWidth = 40
        self.tankHeight = 77
        self.tankSpeed = 1.3

        # Player settings

        self.playersHealthNumber = 3
        self.playersShootCooldown = 2

        # Bullet settings
        self.bulletWidth = 5
        self.bulletHeight = 15
        self.bulletSpeed = 2.8

        # Player settings
        self.playerStartingPostition = {
            "x": 500,
            "y": 300
        }
