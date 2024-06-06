import random

import pygame

from config import DROP_LOOT_EVERYTIME
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_bomb import PickupBomb
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from items.stat_items.categories import Categories
from items.stat_items.item import Item


class Chest(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self.type = type
        self.is_open = False
        self.opened_once = False

        self.groups = self.game.all_sprites, self.game.chest
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * game.settings.TILE_SIZE
        self.y = y * game.settings.TILE_SIZE
        self.width = game.settings.TILE_SIZE
        self.height = game.settings.TILE_SIZE

        self.images = [
            game.image_loader.chests[f"{self.type}_chest{i}"].copy() for i in range(8)
        ]
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self._layer = self.rect.centery

        self.mask = pygame.mask.from_surface(self.image)

        self.current_frame = 0
        self.time_per_frame = 4
        self.timer = self.time_per_frame * (len(self.images) - 1)

    def open(self):
        if not self.opened_once:
            items = []
            self.is_open = True
            self.opened_once = True

            self.drop_loot(items)

            self.game.sound_manager.play_if_not_playing("chestOpen")

            return items

    def update(self):
        if self.is_open and self.timer > 0:
            self.timer -= 1
            if self.timer % self.time_per_frame == 0:
                self.next_frame()

    def next_frame(self):
        self.current_frame += 1
        self.image = self.images[self.current_frame]

    def drop_loot(self, items_to_craft: list):
        if DROP_LOOT_EVERYTIME:  # FOR TESTING PURPOSES
            items_to_craft.append(
                Item(self.game, self.rect.centerx, self.rect.centery, Categories.COMMON)
            )
            items_to_craft.append(
                Item(self.game, self.rect.centerx, self.rect.centery, Categories.EPIC)
            )
            items_to_craft.append(
                Item(
                    self.game,
                    self.rect.centerx,
                    self.rect.centery,
                    Categories.LEGENDARY,
                )
            )
        else:
            if self.type == "small":
                for _ in range(random.randint(1, 2)):
                    items_to_craft.append(
                        SilverCoin(self.game, self.rect.centerx, self.rect.centery)
                    )

                if random.random() < 0.4:
                    items_to_craft.append(
                        GoldenCoin(self.game, self.rect.centerx, self.rect.centery)
                    )

                if random.random() < 0.2:
                    items_to_craft.append(
                        PickupHeart(self.game, self.rect.centerx, self.rect.centery)
                    )

            elif self.type == "medium":
                for _ in range(random.randint(1, 2)):
                    items_to_craft.append(
                        SilverCoin(self.game, self.rect.centerx, self.rect.centery)
                    )

                for _ in range(random.randint(1, 2)):
                    items_to_craft.append(
                        GoldenCoin(self.game, self.rect.centerx, self.rect.centery)
                    )

                if random.random() < 0.5:
                    items_to_craft.append(
                        PickupHeart(self.game, self.rect.centerx, self.rect.centery)
                    )

                for _ in range(random.randint(2, 3)):
                    items_to_craft.append(
                        PickupBomb(self.game, self.rect.centerx, self.rect.centery)
                    )

            elif self.type == "large":
                for _ in range(random.randint(2, 3)):
                    items_to_craft.append(
                        SilverCoin(self.game, self.rect.centerx, self.rect.centery)
                    )

                for _ in range(random.randint(1, 2)):
                    items_to_craft.append(
                        GoldenCoin(self.game, self.rect.centerx, self.rect.centery)
                    )

                items_to_craft.append(
                    PickupHeart(self.game, self.rect.centerx, self.rect.centery)
                )

                for _ in range(random.randint(3, 4)):
                    items_to_craft.append(
                        PickupBomb(self.game, self.rect.centerx, self.rect.centery)
                    )

            item = self.roll_item(self.type)
            if item:
                items_to_craft.append(item)

    def roll_item(self, chest_type):
        match chest_type:
            case "medium":
                category = random.choices(
                    [Categories.COMMON, Categories.EPIC], weights=[0.9, 0.1]
                )[0]
                return Item(self.game, self.rect.centerx, self.rect.centery, category)

            case "large":
                category = random.choices(
                    [Categories.COMMON, Categories.EPIC, Categories.LEGENDARY],
                    weights=[0.6, 0.3, 0.1],
                )[0]
                return Item(self.game, self.rect.centerx, self.rect.centery, category)

            case _:
                return None
