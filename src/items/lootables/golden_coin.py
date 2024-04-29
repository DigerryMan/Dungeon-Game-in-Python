from config import *
from items.lootables.coin import Coin

class GoldenCoin(Coin):
    def __init__(self, game, x, y, drop_animtion = True):
        super().__init__(game, x, y, "gold", drop_animtion)

        self.value = 3