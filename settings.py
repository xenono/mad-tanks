class Settings:
    """
        Class to store some global constants
    """
    def __init__(self):
        # Window settings
        self.screenWidth = 1000
        self.screenHeight = 600
        self.borderSize = 5
        # Tank settings
        self.tankWidth = 50
        self.tankHeight = 76
        self.tankSpeed = 0.3
        # Bullet settings
        self.bulletWidth = 10
        self.bulletHeight = 30
        self.bulletSpeed = 0.5
        # Player settings
        self.playerStartingPostition = {
            "x" : 500,
            "y": 300
        }

