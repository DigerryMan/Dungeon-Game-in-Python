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

        self.is_destroyed = False

    def get_bombed(self):
        if not self.is_destroyed:
            self.is_destroyed = True
            self.game.map.get_current_room().move_block_to_destroyed(self)
            self.game.sound_manager.play_if_not_playing(
                f"rock_crumble{random.randint(1, 3)}"
            )
            self.image = self.game.image_loader.blocks["rock_crumble1"].copy()
            self.mask = pygame.mask.from_surface(self.image)
            self.update_sprite_in_game_sprites()

    def update_sprite_in_game_sprites(self):
        self.game.blocks.remove(self)
        self.game.collidables.remove(self)
        self.game.destroyed_blocks.add(self)
