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

        # Bullet settings
        self.bulletWidth = 10
        self.bulletHeight = 30
        self.bulletSpeed = 0.25

        # Player settings
        self.playerStartingPostition = {
            "x": 500,
            "y": 300
        }
