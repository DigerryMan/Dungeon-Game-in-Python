import pygame
from config import *
from entities.enemy import Enemy

class Fly(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, check_block_colisions=True, 
                         is_wandering=True, bullet_decay_sec=2.0)
        #CHANGEABLE STATS
        self._health = 4
        self._speed = 1
        self._projectal_speed = 4
        self._attack_speed = 2500
        

        #SKINS
        self.image.fill(GREY)

    #Actually running away from the player
    def move_because_of_player(self, chase:bool=False):
        super().move_because_of_player(chase)
    
   
    