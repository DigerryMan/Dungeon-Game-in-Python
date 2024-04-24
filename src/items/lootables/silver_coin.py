from config import *
from items.lootables.coin import Coin

class SilverCoin(Coin):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "silver")
        
        self.value = 1