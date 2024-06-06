import random

import pygame

from items.lootables.golden_coin import GoldenCoin
from items.lootables.silver_coin import SilverCoin
from map.destructable_block import DestructableBlock


class Poop(DestructableBlock):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.type = random.randint(0, 4)
        self.image = game.image_loader.blocks[f"poop{self.type}_4"].copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.durability = 4

    def get_hit(self):
        if self.durability > 0:
            self.durability -= 1
            self.update_image()

        if self.durability == 0 and not self.is_destroyed:
            self.is_destroyed = True
            self.game.sound_manager.play_if_not_playing("fart")
            self.game.map.get_current_room().move_block_to_destroyed(self)
            self.update_sprite_in_game_sprites()
            self.drop_lootable()

    def get_bombed(self):
        if not self.is_destroyed:
            self.is_destroyed = True
            self.durability = 0
            self.game.map.get_current_room().move_block_to_destroyed(self)
            self.game.sound_manager.play_if_not_playing("fart")
            self.image = self.game.image_loader.blocks[f"poop{self.type}_0"].copy()
            self.mask = pygame.mask.from_surface(self.image)
            self.update_sprite_in_game_sprites()
            self.drop_lootable()

    def update_image(self):
        self.image = self.game.image_loader.blocks[
            f"poop{self.type}_{self.durability}"
        ].copy()
        self.mask = pygame.mask.from_surface(self.image)

    def drop_lootable(self):
        rand = random.random()
        room = self.game.map.get_current_room()
        if rand < 0.25:
            if rand < 0.05:
                room.items.append(
                    GoldenCoin(self.game, self.rect.centerx, self.rect.centery)
                )
            else:
                room.items.append(
                    SilverCoin(self.game, self.rect.centerx, self.rect.centery)
                )
