import pygame
import random
from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks, self.game.collidables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * game.settings.TILE_SIZE
        self.y = y * game.settings.TILE_SIZE
        self.width = game.settings.TILE_SIZE
        self.height = game.settings.TILE_SIZE

        self.image = game.image_loader.blocks["rock" + str(random.randint(1, 4))].copy()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y