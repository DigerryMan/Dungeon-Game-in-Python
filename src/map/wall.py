import pygame
from config import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.blocks, self.game.collidables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * game.TILE_SIZE
        self.y = y * game.TILE_SIZE
        self.width = game.TILE_SIZE
        self.height = game.TILE_SIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(DARK_PURPLE)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y