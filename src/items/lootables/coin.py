import random
import pygame
from items.item_types import ItemType
from ..lootable_item import LootableItem

class Coin(LootableItem):
    def __init__(self, game, x, y, type:str, drop_animation=True):
        super().__init__(game, x, y, drop_animation)

        self.value = 0
        self.is_picked_up = False

        self.shine_animation_frame = 0
        self.drop_animation_frame = 0
        self.pickup_animation_frame = 0

        self.shine_interval = random.choice([3, 3.5, 4, 4.5, 5]) * 60
        self.shine_timer = self.shine_interval

        self.type = type # "silver" or "gold"
        
        self.image = game.image_loader.lootables[f"{self.type}_coin_shine0"].copy()
        self.mask = pygame.mask.from_surface(self.image)

        if self.drop_animation_time > 0:
            self.image = game.image_loader.lootables[f"{self.type}_coin_drop0"].copy()


        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.time_per_frame_shine = 3
        self.time_per_frame_drop = self.drop_animation_time // 8
        self.time_per_frame_pickup = 1

        self.pickup_timer = self.time_per_frame_pickup * 9


    def picked_up(self):       
        self.is_picked_up = True
        self.clean_up()
        return ItemType.COIN, self.value
    
    def update(self):
        super().update()
        self.shine_timer = self.shine_timer - 1 if self.shine_timer > 0 else self.shine_interval
        if self.drop_animation_time > 0:
            if self.drop_animation_time % self.time_per_frame_drop == 0:
                self.drop_animation_frame = (self.drop_animation_frame + 1) % 8
                self.image = self.game.image_loader.lootables[f"{self.type}_coin_drop{self.drop_animation_frame}"].copy()

        if not self.is_picked_up and self.shine_timer < 6 * self.time_per_frame_shine:
            if self.shine_timer % self.time_per_frame_shine == 0:
                self.shine_animation_frame = (self.shine_animation_frame + 1) % 6
                self.image = self.game.image_loader.lootables[f"{self.type}_coin_shine{self.shine_animation_frame}"].copy()

        if self.is_picked_up:
            if self.pickup_timer > 0 and self.pickup_timer % self.time_per_frame_pickup == 0:
                self.image = self.game.image_loader.lootables[f"gold_coin_pickup{self.pickup_animation_frame}"].copy()
                self.pickup_animation_frame += 1
            
            elif self.pickup_timer <= 0:
                self.kill()

            self.pickup_timer -= 1