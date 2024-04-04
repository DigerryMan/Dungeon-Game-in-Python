import pygame
from config import *
from utils.directions import Directions

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction:Directions):
        self.is_open = False
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.doors, self.game.collidables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.direction = direction

        self.x = x * game.TILE_SIZE
        self.y = y * game.TILE_SIZE
        self.width = game.TILE_SIZE
        self.height = game.TILE_SIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(YELLOW)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        if self.is_open:
            self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if hits:
            self.game.render_next_room(self.direction)