import random
import pygame

from config import *
from entities.bullet import Bullet
from entities.mobs.maggot import Maggot
from utils.directions import Directions

class AlphaMaggot(Maggot):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        #CHANGEABLE STATS
        self._health = 8
        self._speed = 4
        self._projectal_speed = 3

        #SKIN
        self.image.fill(DARK_RED)

    def attack(self):
        now = pygame.time.get_ticks()
        if now > self._last_shot + self._shot_cd:
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.PLAYER, self._projectal_speed, False)
            self._last_shot = now
            self.roll_next_shot_cd()

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

    