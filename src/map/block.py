import random

import pygame

from config import BLOCK_LAYER


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, is_collidable=True):
        self.game = game
        self._layer = BLOCK_LAYER
        if is_collidable:
            self.groups = self.game.all_sprites, self.game.blocks, self.game.collidables
        else:
            self.groups = self.game.all_sprites, self.game.shop_stands

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

    def get_bombed(self):
        self.kill()
        self.game.map.get_current_room().remove_block(self)
        self.game.sound_manager.play_if_not_playing(
            f"rock_crumble{random.randint(1, 3)}"
        )
