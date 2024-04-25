import pygame
import random
from config import *

class LootableItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y, drop_animtion = True):
        self.game = game
        self._layer = 0
        self.groups = self.game.all_sprites, self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.is_picked_up = False

        if drop_animtion:
            self.drop_animation_time = 40
            self.horizontal_velocity = random.uniform(-3, 3) * game.settings.SCALE
            x = self.horizontal_velocity * self.drop_animation_time
            TS = game.settings.TILE_SIZE
            y = (TS + (5 * TS**2 - 4 * x**2)**0.5)/2
            self.acceleration = 0.2 * game.settings.SCALE
            self.vertical_velocity = (self.y - y - (self.acceleration * self.drop_animation_time**2)/2) / self.drop_animation_time

        else:
            self.drop_animation_time = 0


    def update(self):
        self.drop_animation()

    def drop_animation(self):
        if self.drop_animation_time > 0:
            self.vertical_velocity -= self.acceleration
            self.y -= self.vertical_velocity
            self.x += self.horizontal_velocity
            self.rect.x = round(self.x)
            self.rect.y = round(self.y)
            self.drop_animation_time -= 1

    def picked_up(self):
        pass
    
    def clean_up(self):
        current_room = self.game.map.get_current_room()
        current_room.remove_item(self)