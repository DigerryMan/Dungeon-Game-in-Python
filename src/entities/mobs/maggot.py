import pygame
from config import *
from entities.enemy import Enemy
from utils.directions import Directions

class Maggot(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, False)
        self._speed = 10
        self._health = 3
        self.image.fill(WHITE)
    
    def move(self):
        self.wall_collision()
        if self.facing == Directions.LEFT:
            self.x_change -= self._speed

        if self.facing == Directions.RIGHT:
            self.x_change += self._speed
         
    def attack(self):
        pass

    def wall_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if(hits):
            self.facing = self.facing.reverse()
