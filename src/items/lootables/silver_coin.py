from config import *
from items.lootables.coin import Coin

class SilverCoin(Coin):
    def __init__(self, game, x, y, drop_animtion = True):
        super().__init__(game, x, y, "silver", drop_animtion)
        
        self.value = 1