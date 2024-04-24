from config import *
from items.lootables.coin import Coin

class GoldenCoin(Coin):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "gold")

        self.value = 3