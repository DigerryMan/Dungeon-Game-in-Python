import pygame
from config import FPS

class SatanAnimiation():
    def __init__(self, boss, game):
        self.boss = boss
        self.game = game

        self.img = game.image_loader.bosses["satan"]
        self.images = []
        self.prepare_images()

        self.boss.image = self.images[0]
        self.boss.mask = pygame.mask.from_surface(self.boss.image)

        self.time = self.time_cd = 10
        self.index = 0
        
        #bullets from hands
        self.frame_index = 0

        #SHAKING
        self.shake_time_left = 5
        self.change = 1

        self.shake_time_y_left = 5
        self.y_change = 1

    def animate(self):
        if self.boss.bullets_from_hands_active:
            self.shaking_animation()
            self.shaking_animation_y()
            self.animate_bullets_from_hands()
        elif self.boss.laser_breath_active:
            self.shaking_animation(True)
            self.animate_laser_breath()
   
    def animate_bullets_from_hands(self):        
        frames = [1, 13, 14, 15, 1]
        time_stages = [0.99, 0.8, 0.49, 0.4, 0.12]
        time_stages = [int(time * self.boss.bullets_from_hands_period) for time in time_stages]
        if self.boss.bullets_from_hands_time in time_stages:
            self.boss.image = self.images[frames[self.frame_index]]
            self.frame_index += 1
            self.frame_index %= len(time_stages)

    def animate_laser_breath(self):
        frames = [7, 3, 7, 9, 10, 7, 1, 0]
        time_stages = [0.99, 0.95, 0.87, 0.75, 0.42, 0.3, 0.2, 0.1]
        time_stages = [int(time * self.boss.laser_breath_period) for time in time_stages]
        if self.boss.laser_breath_time in time_stages:
            self.boss.image = self.images[frames[self.frame_index]]
            self.frame_index += 1
            self.frame_index %= len(time_stages)

    def prepare_images(self):
        size = self.boss.MOB_WIDTH, self.boss.MOB_HEIGHT
        for y in range(6):
            for x in range(4):
                image = self.img.subsurface(pygame.Rect(x * 200, y * 120, 200, 120))
                self.images.append(pygame.transform.scale(image, size))

        image = self.img.subsurface(pygame.Rect(4 * 200, 2 * 120, 200, 120))
        self.images.append(pygame.transform.scale(image, size))

        image = self.img.subsurface(pygame.Rect(4 * 200,  0, 200, 240))
        self.images.append(pygame.transform.scale(image, size))
    
    def shaking_animation(self, with_laser=False):
        self.shake_time_left -= 1
        if self.shake_time_left <= 0:
            self.boss.rect.centerx += 5 * self.change
            if with_laser and self.boss.laser is not None:
                self.boss.laser.rect.centerx += 5 * self.change
            
            self.change *= -1
            self.shake_time_left = 3

    def shaking_animation_y(self):
        self.shake_time_y_left -= 1
        if self.shake_time_y_left <= 0:
            self.boss.rect.centery += 2 * self.change
            self.y_change *= -1
            self.shake_time_y_left = 9