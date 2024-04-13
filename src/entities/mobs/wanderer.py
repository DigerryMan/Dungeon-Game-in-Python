from entities.enemy import Enemy

class Wanderer(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)

    @staticmethod
    def check_group_attacked():
        return Wanderer.is_group_attacked

    @staticmethod
    def group_attacked():
        Wanderer.is_group_attacked = True