import random
import pygame
from config import FPS
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
        self.curr_frame = 0
        self.img = game.image_loader.get_image("parasite")
        self.prepare_images()
        self.image = self.images[0]
        self.unchanged_image = self.image.copy()

        #REST
        self.is_dig = True
        self.already_shot = False
        self.diging_time_left = self._dig_cooldown
        self.time_left_to_shoot = self.shoot_cd_after_dig_out

        self.change_dmg_vulnerability(self.is_dig)

    def prepare_images(self):
        for x in range(8):
            self.images.append(self.img.subsurface(pygame.Rect(x * self.MOB_SIZE, 0, self.MOB_SIZE, self.MOB_SIZE)))

    def move(self):
        self.diging_time_left -= 1
        if self.diging_time_left <= 0:
            self.diging_time_left = self._dig_cooldown
            if self.is_dig: #wykopanie
                self.is_dig = False
                self.change_dmg_vulnerability(True)

            else:           #zakopanie
                self.is_dig = True
                self.already_shot = False
                self.change_dmg_vulnerability(False)

    def attack(self):
        if not self.is_dig and not self.already_shot:
            self.time_left_to_shoot -= 1
            if self.time_left_to_shoot <= 0:
                Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.PLAYER, is_friendly = False)
                self.already_shot = True
                self.time_left_to_shoot = self.shoot_cd_after_dig_out
    
    def collide_player(self):
        if not self.is_dig:
            super().collide_player()

    def change_dmg_vulnerability(self, is_vulnerable: bool):
        if is_vulnerable:
            self.game.not_voulnerable.remove(self)
        else:
            self.game.not_voulnerable.add(self)
    
    def animate(self):
        if self.diging_time_left == int(self._dig_cooldown * 0.25):
            self.nextFrame()
        elif self.diging_time_left == int(self._dig_cooldown * 0.125):
            self.nextFrame()
        elif self.diging_time_left == int(self._dig_cooldown * 0.05):
            self.nextFrame()
        
        if not self.is_dig:
            if self.time_left_to_shoot == int(0.4 * self.shoot_cd_after_dig_out):
                self.nextFrame(player_shoot_frame=True)
            if self.time_left_to_shoot == int(0.2 * self.shoot_cd_after_dig_out):
                self.nextFrame()
        
        super().animate()

    def nextFrame(self, player_shoot_frame=False):
        self.is_change_of_frame = True
        self.curr_frame = (self.curr_frame + 1) % 8 
        self.frame = self.images[self.curr_frame]
        self.sound_managment()        
        
        if player_shoot_frame:
            x_p, _ = self.game.player.get_center_position()
            if x_p < self.rect.centerx:
                self.frame = pygame.transform.flip(self.frame, True, False)

        self.remove_transparency_from_frame()
       
    
    def remove_transparency_from_frame(self):
        old_x_center = self.rect.centerx
        old_bottom = self.rect.bottom

        bounding_rect = self.frame.get_bounding_rect() 
        self.image = self.frame.subsurface(bounding_rect)
        self.unchanged_image = self.image.copy()

        self.rect.width, self.rect.height = self.image.get_rect().width, self.image.get_rect().height
        self.rect.bottom = old_bottom
        self.rect.centerx = old_x_center

    def sound_managment(self):
        if self.curr_frame == 1:
            self.play_audio(f"parasiteBurstOut{random.randint(1, 2)}")
        elif self.curr_frame == 6:
            self.play_audio(f"parasiteEnterGround{random.randint(1, 2)}")