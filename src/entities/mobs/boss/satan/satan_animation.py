import pygame
from config import FPS

class SatanAnimiation():
    def __init__(self, boss, game, _skin:str="satan"):
        self.boss = boss
        self.game = game

        self.img = game.image_loader.bosses[_skin]
        self.images = []
        self.prepare_images()

        self.boss.image = self.images[21]
        self.boss.mask = pygame.mask.from_surface(self.boss.image)

        self.intro_image = None
        self.intro_name = None
        self.prepare_intro_images(_skin)

        self.time = self.time_cd = 10
        self.index = 0
        
        #bullets from hands
        self.frame_index = 0

        #SHAKING
        self.shake_time_left = 5
        self.change = 1

        self.shake_time_y_left = 5
        self.y_change = 1

    def prepare_intro_images(self, _skin:str="satan"):
        if _skin == "satan":
            img = self.img.subsurface(pygame.Rect(30, 752, 159, 163))
            self.intro_image = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))
            img = self.img.subsurface(pygame.Rect(237, 805, 122, 38))
            self.intro_name = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))
        else:
            img = self.img.subsurface(pygame.Rect(30, 752, 159, 163))
            self.intro_image = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))
            img = self.img.subsurface(pygame.Rect(237, 805, 170, 38))
            self.intro_name = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))

    def animate(self):
        if self.boss.boss_figth_start_active:
            self.waking_up_animation()
        elif self.boss.bullets_from_hands_active:
            self.shaking_animation()
            self.shaking_animation_y()
            self.animate_bullets_from_hands()
        elif self.boss.laser_breath_active:
            self.shaking_animation(True)
            self.animate_laser_breath()
        elif self.boss.mouth_attack_active:
            self.shaking_animation()
            self.animate_mouth_attack()
        elif self.boss.flying_active:
            self.flying_animation()
            self.shaking_animation()
            self.shaking_animation_y()
            
    def waking_up_animation(self):
        frames = [21, 22, 23, 1]
        time_stages = [0.99, 0.2, 0.12, 0.06]
        time_stages = [int(time * self.boss.bullets_from_hands_period) for time in time_stages]
        if self.boss.start_time in time_stages:
            self.boss.image = self.images[frames[self.frame_index]]
            self.boss.mask = pygame.mask.from_surface(self.boss.image)
            self.frame_index += 1
            self.frame_index %= len(time_stages)
            
    def animate_bullets_from_hands(self):        
        frames = [1, 13, 14, 15, 1]
        time_stages = [0.99, 0.8, 0.49, 0.4, 0.12]
        time_stages = [int(time * self.boss.bullets_from_hands_period) for time in time_stages]
        if self.boss.bullets_from_hands_time in time_stages:
            self.boss.image = self.images[frames[self.frame_index]]
            self.boss.mask = pygame.mask.from_surface(self.boss.image)
            self.frame_index += 1
            self.frame_index %= len(time_stages)

    def animate_laser_breath(self):
        frames = [7, 3, 7, 9, 10, 7, 1, 0]
        time_stages = [0.99, 0.95, 0.87, 0.75, 0.42, 0.3, 0.2, 0.1]
        time_stages = [int(time * self.boss.laser_breath_period) for time in time_stages]
        if self.boss.laser_breath_time in time_stages:
            self.boss.image = self.images[frames[self.frame_index]]
            self.boss.mask = pygame.mask.from_surface(self.boss.image)
            self.frame_index += 1
            self.frame_index %= len(time_stages)

    def animate_mouth_attack(self):
        frames = [1, 2, 6, 8, 0, 1]
        time_stages = [0.99, 0.92, 0.83, 0.55, 0.25, 0.05]
        time_stages = [int(time * self.boss.mouth_attack_period) for time in time_stages]
        if self.boss.mouth_attack_time in time_stages:
            self.boss.image = self.images[frames[self.frame_index]]
            self.boss.mask = pygame.mask.from_surface(self.boss.image)
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

        image = self.img.subsurface(pygame.Rect(4 * 200, 3 * 120, 200, 120))
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
            self.boss.rect.centery += 2 * self.y_change
            self.y_change *= -1
            self.shake_time_y_left = 7

    def flying_animation(self):
        frames = [1, 25]
        time_stages = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        time_stages = [int(time * self.boss.flying_period) for time in time_stages]
        if self.boss.flying_time in time_stages:
            self.boss.image = self.images[frames[self.frame_index]]
            self.boss.mask = pygame.mask.from_surface(self.boss.image)
            self.frame_index += 1
            self.frame_index %= len(frames)
            if self.boss.flying_time == time_stages[len(time_stages) - 1]:
                self.frame_index = 0