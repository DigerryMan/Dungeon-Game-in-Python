import pygame
from config import *

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction:str):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.direction = direction

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(YELLOW)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if hits:
            self.game.render_next_room(self.direction)  