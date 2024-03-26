import pygame
from config import *
from entities.bullet import Bullet
from utils.directions import Directions
from ..enemy import Enemy

class Parasite(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, False, False)
        self._health = 3
        self.image.fill(BROWN)
        self._dig_cooldown = 1500
        self.shoot_after_dig_out = 700
        self.shot = False
        self.last_dig = pygame.time.get_ticks()
        self.last_dig_out = 0
        self.is_dig = True
        self.change_dmg_vulnerability(self.is_dig)

    def move(self):
        now = pygame.time.get_ticks()
        if self.is_dig:
            self.image.fill(BROWN)
            if now - self.last_dig > self._dig_cooldown: #wykopanie
                self.is_dig = False
                self.last_dig_out = now
                self.change_dmg_vulnerability(True)

        else:
            self.image.fill(GREEN)
            if now - self.last_dig_out > self._dig_cooldown: #zakopanie
                self.is_dig = True
                self.last_dig = now
                self.shot = False
                self.change_dmg_vulnerability(False)

    def attack(self):
        if not self.is_dig:
            now = pygame.time.get_ticks()
            if now > self.last_dig_out + self.shoot_after_dig_out and not self.shot:
                Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.PLAYER, is_friendly = False)
                self.shot = True
    
    def collide_player(self):
        if not self.is_dig:
            hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits:
                self.game.damage_player(self._collision_damage)
                self.game.playing = False

    def change_dmg_vulnerability(self, is_on: bool):
        if is_on:
            self.game.not_voulnerable.remove(self)
        else:
            self.game.not_voulnerable.add(self)

    