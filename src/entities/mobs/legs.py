from ..enemy import *

class Legs(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, True, False)
        self._speed = 2
        self._health = 5
        self.image.fill(PURPLE)
    
    def attack(self):
        pass
    

