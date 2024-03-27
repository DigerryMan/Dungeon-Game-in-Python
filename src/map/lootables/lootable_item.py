import pygame
import random
from config import *

class Lootable_item(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = 0
        self.groups = self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.horizontal_velocity = random.uniform(-3, 3)
        self.vertical_velocity = 10 - abs(self.horizontal_velocity) * 1.5
        self.acceleration = 1.05 - abs(self.horizontal_velocity) / 6
        self.vertical_travel_time = 0

        
        self.x = x
        self.y = y
        self.width = TILE_SIZE // 5
        self.height = TILE_SIZE // 10

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.drop_animation()
        self.picked_up()

    def drop_animation(self):
        if self.vertical_travel_time < 22:
            self.vertical_velocity -= self.acceleration
            self.y -= self.vertical_velocity
            self.x += self.horizontal_velocity
            self.rect.x = round(self.x)
            self.rect.y = round(self.y)
            self.vertical_travel_time += 1

    def picked_up(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        
        if hits:
            current_room = self.game.map.get_current_room()
            current_room.remove_item(self)
            print("Item picked up")
            self.kill()