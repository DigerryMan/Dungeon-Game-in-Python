import pygame
from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.blocks, self.game.collidables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * game.settings.TILE_SIZE
        self.y = y * game.settings.TILE_SIZE
        self.width = game.settings.TILE_SIZE
        self.height = game.settings.TILE_SIZE

        #self.img = game.image_loader.get_image("rocks2")
        #self.image = self.img.subsurface(pygame.Rect(5, 5, 51, 55))
        #self.image = pygame.transform.smoothscale(self.image, (self.game.settings.TILE_SIZE, self.game.settings.TILE_SIZE))
        self.image = game.image_loader.blocks["bright_rock1"]
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y