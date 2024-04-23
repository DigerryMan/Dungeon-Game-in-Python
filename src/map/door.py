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

        self.x = x * game.settings.TILE_SIZE
        self.y = y * game.settings.TILE_SIZE
        self.width = game.settings.TILE_SIZE
        self.height = game.settings.TILE_SIZE

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.x
        self.rect.y = self.y

        self.image = game.image_loader.doors["basement_door1"].copy()

        if direction == Directions.UP:
            x = self.rect.centerx
            self.rect.width = self.image.get_width()
            self.rect.centerx = x
            self.x = self.rect.x

        elif direction == Directions.DOWN:
            self.image = pygame.transform.rotate(self.image, 180)
            x = self.rect.centerx
            self.rect.width = self.image.get_width()
            self.rect.centerx = x
            self.x = self.rect.x

        elif direction == Directions.LEFT:
            self.image = pygame.transform.rotate(self.image, 90)

        elif direction == Directions.RIGHT:
            self.image = pygame.transform.rotate(self.image, -90)


    def update(self):
        self.draw()
        if self.is_open:
            self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if hits:
            mask_hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False, pygame.sprite.collide_mask)
            if mask_hits:
                self.game.render_next_room(self.direction)
    def open(self):
        self.is_open = True