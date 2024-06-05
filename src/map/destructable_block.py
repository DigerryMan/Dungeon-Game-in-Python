import random

import pygame

from .block import Block


class DestructableBlock(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.image = game.image_loader.blocks["vase" + str(random.randint(1, 4))].copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.durability = 3

    def get_hit(self):
        if self.durability > 0:
            self.durability -= 1

        if self.durability == 0 and not self.is_destroyed:
            self.is_destroyed = True
            self.game.sound_manager.play_if_not_playing(
                f"rock_crumble{random.randint(1, 3)}"
            )
            self.game.map.get_current_room().move_block_to_destroyed(self)
            self.image = self.game.image_loader.blocks["rock_crumble2"].copy()
            self.mask = pygame.mask.from_surface(self.image)
            self.update_sprite_in_game_sprites()

    def get_bombed(self):
        if not self.is_destroyed:
            super().get_bombed()
            self.image = self.game.image_loader.blocks["rock_crumble2"].copy()
            self.mask = pygame.mask.from_surface(self.image)
