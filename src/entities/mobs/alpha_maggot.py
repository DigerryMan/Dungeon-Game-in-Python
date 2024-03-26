import random
import pygame

from config import PURPLE
from entities.mobs.maggot import Maggot

class AlphaMaggot(Maggot):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self._health = 8
        self._speed = 4
        self.image.fill(PURPLE)

    def random_change_of_direction(self):
        now = pygame.time.get_ticks()
        if now - self._last_change_of_direction > self._random_dir_change_cd:
            self._last_change_of_direction = now
            
            self.rotate_facing()
    
    def rotate_facing(self):
        rand = random.randint(1, 3)

        if rand == 1:
            self.facing = self.facing.rotate_clockwise()
        elif rand == 2:
            self.facing = self.facing.rotate_counter_clockwise()
        else:
            self.facing = self.facing.reverse()
            

        self.roll_rotation_cd(300,1800)
        self._last_change_of_direction = pygame.time.get_ticks()