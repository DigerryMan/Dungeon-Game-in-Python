import random

import pygame

from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_bomb import PickupBomb
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin

from .block import Block


class TreasureBlock(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.is_bomb_treasure = random.random() < 0.15

        if self.is_bomb_treasure:
            self.image = game.image_loader.blocks["treasure_rock_bomb"].copy()
        else:
            self.image = game.image_loader.blocks[
                "treasure_rock" + str(random.randint(1, 2))
            ].copy()

        self.prepare_mask()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def get_bombed(self):
        if not self.is_destroyed:
            super().get_bombed()
            self.drop_lootable()

    def drop_lootable(self):
        if self.is_bomb_treasure:
            for _ in range(random.randint(3, 4)):
                self.game.map.get_current_room().items.append(
                    PickupBomb(self.game, self.rect.centerx, self.rect.centery)
                )
        else:
            rand = random.random()
            room = self.game.map.get_current_room()
            if rand < 0.5:
                room.items.append(
                    SilverCoin(self.game, self.rect.centerx, self.rect.centery)
                )
            elif rand < 0.8:
                room.items.append(
                    GoldenCoin(self.game, self.rect.centerx, self.rect.centery)
                )
            else:
                room.items.append(
                    PickupHeart(self.game, self.rect.centerx, self.rect.centery)
                )
