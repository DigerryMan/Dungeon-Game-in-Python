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
        self.prepare_mask()

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
            self.update_sprite_in_game_sprites()

    def update_sprite_in_game_sprites(self):
        self.game.blocks.remove(self)
        self.game.collidables.remove(self)
        self.game.destroyed_blocks.add(self)

    def prepare_mask(self):
        mask_width = int(self.width * 0.9)
        mask_height = int(self.height * 0.9)

        mask_surface = pygame.Surface((mask_width, mask_height))
        mask_surface.fill((0, 0, 0))

        self.mask = pygame.mask.from_surface(mask_surface)
        self.mask = self.correct_mask(self.mask)

    def correct_mask(self, mask):
        removed_hitbox_from_left = pygame.Surface((self.width * 0.1, self.height))
        removed_hitbox_from_bottom = pygame.Surface((self.width, self.height * 0.3))

        cut_mask_left = pygame.mask.from_surface(removed_hitbox_from_left)
        cut_mask_bottom = pygame.mask.from_surface(removed_hitbox_from_bottom)

        mask.erase(cut_mask_left, (0, 0))
        mask.erase(cut_mask_bottom, (0, self.height - cut_mask_bottom.get_size()[1]))

        return mask
