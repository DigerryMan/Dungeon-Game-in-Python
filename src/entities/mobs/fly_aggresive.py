import random

import pygame
from entities.mobs.fly import Fly

class FlyAggresive(Fly):
    is_group_attacked = True
    def __init__(self, game, x, y, boss):
        super().__init__(game, x, y, False)
        self.boss = boss
        self._max_health = 4
        self._health = self._max_health
        self._damage = 0.5
        self._speed = 2 * game.settings.SCALE
        self._projectal_speed = 9
        self._bullet_decay_sec = 0.5


        self.will_chase = random.choice([True, False])
        self.prepare_images_v2()
        self.image = self.images[0]

    def prepare_images_v2(self): 
        self.images[0] = self.img.subsurface(pygame.Rect(1 * self.MOB_SIZE, 1 * self.MOB_SIZE, self.MOB_SIZE, self.MOB_SIZE))     
        self.images[1] = self.img.subsurface(pygame.Rect(2 * self.MOB_SIZE, 1 * self.MOB_SIZE, self.MOB_SIZE, self.MOB_SIZE)) 

    def move_because_of_player(self, chase=False):
        super().move_because_of_player(self.will_chase)
    
    def collide_blocks(self, orientation:str):
        rect_hits_collidables = pygame.sprite.spritecollide(self, self.game.collidables, False)
        rect_hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        try:
            rect_hits_enemies.remove(self)
            rect_hits_enemies.remove(self.boss)
        except ValueError:
            pass
        
        if rect_hits_collidables:
           self.revert_move(orientation)
        elif rect_hits_enemies:
            mask_hits = self.get_mask_colliding_sprite(rect_hits_enemies)
            if mask_hits:
                self.revert_move(orientation)

    def revert_move(self, orientation:str):
        if orientation == 'x':
            self.rect.x -= self.x_change
        if orientation == 'y':
            self.rect.y -= self.y_change

    def get_mask_colliding_sprite(self, rect_hits):
        for sprite in rect_hits:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite
        return None
    
    def collide_beetwen_mobs(self, orientation:str):
        rect_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if len(rect_hits) > 1:
            if orientation == 'x':
                self.rect.x -= self.x_change

            if orientation == 'y':
                self.rect.y -= self.y_change