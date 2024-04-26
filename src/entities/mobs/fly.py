from config import *
from entities.enemy import Enemy

class Fly(Enemy):
    is_group_attacked = False
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, check_block_colisions=True, 
                         is_wandering=True, bullet_decay_sec=2.0)
        #CHANGEABLE STATS
        self._health = 4
        self._speed = 1 * game.settings.WINDOW_SIZE_SPEED_FACTOR
        self._projectal_speed = 6
        self._shot_cd = int(2.4 * FPS)
        print(Fly.is_group_attacked)
        #SKINS
        self.image.fill(GREY)

    #Actually running away from the player
    def move_because_of_player(self, chase:bool=False):
        super().move_because_of_player(chase)
    
    @staticmethod
    def check_group_attacked():
        return Fly.is_group_attacked

    @staticmethod
    def group_attacked():
        Fly.is_group_attacked = True