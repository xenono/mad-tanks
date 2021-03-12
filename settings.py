class Settings:
    """
        Class to store some global constants
    """

    def __init__(self):
        # Window settings
        self.screenWidth = 1400
        self.screenHeight = 900
        self.borderSize = 5

        # Tank settings
        self.tankWidth = 40
        self.tankHeight = 77
        self.tankSpeed = 0.2

        # Player settings

        self.playersHealthNumber = 3
        self.playersShootCooldown = 2

        # Bullet settings
        self.bulletWidth = 5
        self.bulletHeight = 15
        self.bulletSpeed = 1

        # Player settings
        self.playerStartingPostition = {
            "x": 500,
            "y": 300
        }
