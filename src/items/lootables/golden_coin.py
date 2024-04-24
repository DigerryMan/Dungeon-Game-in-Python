import random
import pygame
from config import *
from ..lootable_item import LootableItem

class GoldenCoin(LootableItem):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.is_picked_up = False

        self.shine_animation_frame = 0
        self.drop_animation_frame = 0
        self.pickup_animation_frame = 0

        self.shine_interval = random.choice([3, 3.5, 4, 4.5, 5]) * 60
        self.shine_timer = self.shine_interval

        if self.drop_animation_time > 0:
            self.image = game.image_loader.lootables["gold_coin_drop0"]

        else:
            self.image = game.image_loader.lootables["gold_coin_shine0"]

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.time_per_frame_shine = 3
        self.time_per_frame_drop = self.drop_animation_time // 8
        self.time_per_frame_pickup = 4

        self.pickup_timer = self.time_per_frame_pickup * 9

        self.mask = pygame.mask.from_surface(self.image)


    def picked_up(self):
        if self.is_picked_up:
            return 0
        
        self.is_picked_up = True
        return 3
    
    def update(self):
        super().update()
        self.shine_timer = self.shine_timer - 1 if self.shine_timer > 0 else self.shine_interval
        if self.drop_animation_time > 0:
            if self.drop_animation_time % self.time_per_frame_drop == 0:
                self.drop_animation_frame = (self.drop_animation_frame + 1) % 8
                self.image = self.game.image_loader.lootables[f"gold_coin_drop{self.drop_animation_frame}"]

        if not self.is_picked_up and self.shine_timer < 6 * self.time_per_frame_shine:
            if self.shine_timer % self.time_per_frame_shine == 0:
                self.shine_animation_frame = (self.shine_animation_frame + 1) % 6
                self.image = self.game.image_loader.lootables[f"gold_coin_shine{self.shine_animation_frame}"]

        if self.is_picked_up:
            if self.pickup_timer > 0 and self.pickup_timer % self.time_per_frame_pickup == 0:
                self.image = self.game.image_loader.lootables[f"gold_coin_pickup{self.pickup_animation_frame}"]
                self.pickup_animation_frame += 1
            
            elif self.pickup_timer <= 0:
                self.clean_up()
                self.kill()

            self.pickup_timer -= 1