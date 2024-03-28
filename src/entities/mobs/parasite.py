import pygame
from config import *
from entities.bullet import Bullet
from utils.directions import Directions
from ..enemy import Enemy

class Parasite(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, False, False)
        #CHANGEABLE STATS
        self._health = 3 
        self._dig_cooldown = 1500
        self.shoot_cd_after_dig_out = 700

        #SKIN
        self.image.fill(BROWN)

        #REST
        self.already_shot = False
        self.last_dig = pygame.time.get_ticks()
        self.last_dig_out = 0
        self.is_dig = True

        self.change_dmg_vulnerability(self.is_dig)

    def move(self):
        now = pygame.time.get_ticks()
        if self.is_dig:
            self.image.fill(BROWN) #zakopany
            if now - self.last_dig > self._dig_cooldown: #wykopanie
                self.is_dig = False
                self.last_dig_out = now
                self.change_dmg_vulnerability(True)

        else:
            self.image.fill(GREEN) #odkopany
            if now - self.last_dig_out > self._dig_cooldown: #zakopanie
                self.is_dig = True
                self.last_dig = now
                self.already_shot = False
                self.change_dmg_vulnerability(False)

    def attack(self):
        if not self.is_dig:
            now = pygame.time.get_ticks()
            if (now > self.last_dig_out + self.shoot_cd_after_dig_out) and not self.already_shot:
                Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.PLAYER, is_friendly = False)
                self.already_shot = True
    
    def collide_player(self):
        if not self.is_dig:
            hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits:
                self.game.damage_player(self._collision_damage)

    def change_dmg_vulnerability(self, is_vulnerable: bool):
        if is_vulnerable:
            self.game.not_voulnerable.remove(self)
        else:
            self.game.not_voulnerable.add(self)

    