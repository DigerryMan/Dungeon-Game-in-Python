import pygame
from config import *
from entities.enemy import Enemy

class Ghost(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, check_block_colisions=False, 
                         is_wandering=False, bullet_decay_sec=3)
        
        #CHANGEABLE STATS
        self._health = 6
        self._speed = 3
        self._projectal_speed = 7
        
        #SKINS
        self.image.fill(CYAN)

    def correct_layer(self):
        self._layer = 3000
