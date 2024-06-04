from items.lootables.coin import Coin


class SilverCoin(Coin):
    def __init__(self, game, x, y, drop_animation=True):
        super().__init__(game, x, y, "silver", drop_animation)

        self.value = 1
