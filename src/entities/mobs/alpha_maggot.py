import random
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
        self.img = game.image_loader.get_image("alpha_maggot")

    def attack(self):
        self._shot_time_left -= 1
        if self._shot_time_left <= 0:
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.PLAYER, 
                   self._projectal_speed, False, time_decay_in_seconds=1.5)
            self.roll_next_shot_cd()
            self._shot_time_left = self._shot_cd

    def rotate_facing(self):
        rand = random.randint(1, 3)

        if rand == 1:
            self.facing = self.facing.rotate_clockwise()
        elif rand == 2:
            self.facing = self.facing.rotate_counter_clockwise()
        else:
            self.facing = self.facing.reverse()
            
        self.roll_rotation_cd(int(0.3 * FPS), int(1.8 * FPS))