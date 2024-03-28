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
        self._random_dir_change_cd = 2000
        
        #SKIN
        self.image.fill(WHITE)

        #REST
        self.moving_clockwise = moving_clockwise
        self._last_change_of_direction = pygame.time.get_ticks()
        
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
                self.rect.x = hits[0].rect.left - TILE_SIZE

            elif self.facing == Directions.UP:
                self.rect.y = hits[0].rect.bottom

            elif self.facing == Directions.DOWN:
                self.rect.y = hits[0].rect.top - TILE_SIZE

            self.rotate_facing()
            
    def random_change_of_direction(self):
        now = pygame.time.get_ticks()
        if now - self._last_change_of_direction > self._random_dir_change_cd:
            self._last_change_of_direction = now
            
            self.rotate_facing()

    def rotate_facing(self):
        if self.moving_clockwise:
            self.facing = self.facing.rotate_clockwise()
        else:
            self.facing = self.facing.rotate_counter_clockwise()

        self.roll_rotation_cd(400, 2200)
        self._last_change_of_direction = pygame.time.get_ticks()
        
    def roll_rotation_cd(self, mini:int, maxi:int):
        self._random_dir_change_cd = random.randint(mini, maxi)