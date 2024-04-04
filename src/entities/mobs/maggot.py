import random
import pygame
from config import *
from entities.enemy import Enemy
from utils.directions import Directions

class Maggot(Enemy):
    def __init__(self, game, x, y, moving_clockwise=random.choice([True, False])):
        super().__init__(game, x, y, False)
        #CHANGEABLE STATS
        self._health = 4
        self._speed = 3
        self._random_dir_change_cd = int(2 * FPS)
        
        #SKIN
        self.image.fill(WHITE)

        #REST
        self.moving_clockwise = moving_clockwise
        self._change_of_direction_time_left = self._random_dir_change_cd
        
        
    def move(self):
        self.wall_collision()
        self.random_change_of_direction()
        if self.facing == Directions.LEFT:
            self.x_change -= self._speed

        if self.facing == Directions.RIGHT:
            self.x_change += self._speed
        
        if self.facing == Directions.UP:
            self.y_change -= self._speed

        if self.facing == Directions.DOWN:
            self.y_change += self._speed
        
    def attack(self):
        pass

    def wall_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.collidables, False)

        if hits:
            if self.facing == Directions.LEFT:
                self.rect.x = hits[0].rect.right 

            elif self.facing == Directions.RIGHT:
                self.rect.x = hits[0].rect.left - self.game.settings.TILE_SIZE

            elif self.facing == Directions.UP:
                self.rect.y = hits[0].rect.bottom

            elif self.facing == Directions.DOWN:
                self.rect.y = hits[0].rect.top - self.game.settings.TILE_SIZE

            self.rotate_facing()
            
    def random_change_of_direction(self):
        self._change_of_direction_time_left -= 1
        if self._change_of_direction_time_left <= 0:
            self.roll_rotation_cd(int(0.4 * FPS), int(2.2 * FPS))
            self._change_of_direction_time_left = self._random_dir_change_cd
            
            self.rotate_facing()

    def rotate_facing(self):
        if self.moving_clockwise:
            self.facing = self.facing.rotate_clockwise()
        else:
            self.facing = self.facing.rotate_counter_clockwise()

        
    def roll_rotation_cd(self, mini:int, maxi:int):
        self._random_dir_change_cd = random.randint(mini, maxi)