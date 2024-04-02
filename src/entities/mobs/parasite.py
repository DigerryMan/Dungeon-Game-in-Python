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
        self._dig_cooldown = int(1.5 * FPS)
        self.shoot_cd_after_dig_out = int(0.7 * FPS)

        #SKIN
        self.image.fill(BROWN)

        #REST
        self.is_dig = True
        self.already_shot = False
        self.diging_time_left = self._dig_cooldown
        self.time_left_to_shoot = self.shoot_cd_after_dig_out

        self.change_dmg_vulnerability(self.is_dig)

    def move(self):
        self.diging_time_left -= 1
        if self.diging_time_left <= 0:
            self.diging_time_left = self._dig_cooldown
            if self.is_dig: #wykopanie
                self.is_dig = False
                self.change_dmg_vulnerability(True)
                self.image.fill(GREEN) #odkopany

            else:           #zakopanie
                self.is_dig = True
                self.already_shot = False
                self.change_dmg_vulnerability(False)
                self.image.fill(BROWN) #zakopany

    def attack(self):
        if not self.is_dig and not self.already_shot:
            self.time_left_to_shoot -= 1
            if self.time_left_to_shoot <= 0:
                Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.PLAYER, is_friendly = False)
                self.already_shot = True
                self.time_left_to_shoot = self.shoot_cd_after_dig_out
    
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