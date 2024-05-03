from items.lootables.coin import Coin

class GoldenCoin(Coin):
    def __init__(self, game, x, y, drop_animation=True):
        super().__init__(game, x, y, "gold", drop_animation)

        self.value = 3