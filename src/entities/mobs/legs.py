from ..enemy import *

class Legs(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, True, is_wandering=False)
        self._speed = 3 * game.settings.WINDOW_SIZE_SPEED_FACTOR
        self._health = 5
        self.image.fill(PURPLE)
    
    def attack(self):
        pass
    

