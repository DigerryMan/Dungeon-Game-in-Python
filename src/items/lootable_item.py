import pygame
import random
from config import *

class LootableItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = 0
        self.groups = self.game.all_sprites, self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.horizontal_velocity = random.uniform(-5, 5)
        self.vertical_velocity = 10 - abs(self.horizontal_velocity) * 1.5
        self.acceleration = 1.05 - abs(self.horizontal_velocity) / 6
        self.vertical_travel_time = 0

        
        self.x = x
        self.y = y
        self.width = game.settings.TILE_SIZE // 5
        self.height = game.settings.TILE_SIZE // 10

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.drop_animation()

    def drop_animation(self):
        if self.vertical_travel_time < 26:
            self.vertical_velocity -= self.acceleration
            self.y -= self.vertical_velocity
            self.x += self.horizontal_velocity
            self.rect.x = round(self.x)
            self.rect.y = round(self.y)
            self.vertical_travel_time += 1

    def picked_up(self):
        self.clean_up()
        return None
    
    def clean_up(self):
        current_room = self.game.map.get_current_room()
        current_room.remove_item(self)
        self.kill()