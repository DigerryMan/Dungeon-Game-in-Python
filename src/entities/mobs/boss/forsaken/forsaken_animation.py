import pygame
from config import FPS

class ForsakenAnimation():
    def __init__(self, boss, game):
        self.boss = boss
        self.game = game
        self.img = game.image_loader.bosses["forsaken"]
        self.images = []
        self.prepare_images()
        self.boss.image = self.images[0]
        self.boss.mask = pygame.mask.from_surface(self.boss.image)

        self.time = 20
        self.time_cd = 20
        self.frame_index = 0

        #SHAKING
        self.change = 1
        self.y_change = 1

        self.shake_time_left = 0
        self.shake_time_y_left = 0

    def prepare_images(self):
        end = 4
        for y in range(3):
            for x in range(end):
                image = self.img.subsurface(pygame.Rect(x * 95, y * 92, 95, 92))
                self.images.append(pygame.transform.scale(image, (self.boss.MOB_SIZE, self.boss.MOB_SIZE)))
            if y == 1:
                end = 3

    def animate(self):
        if self.boss.lasers_active:
            self.laser_animation()
        else:
            self.time -= 1
            if self.time <= 0:
                self.time = self.time_cd
                self.boss.image = self.images[self.frame_index]
                self.frame_index += 1
                self.frame_index %= len(self.images)
    
    def laser_animation(self):
        self.boss.image = self.change_opacity(self.images[5], 100)
        self.shaking_animation()
        self.shaking_animation_y()

    def change_opacity(self, image, opacity=50):
        image = image.copy()
        if 0 <= opacity <= 255:
            for x in range(image.get_width()):
                for y in range(image.get_height()):
                    r, g, b, a = image.get_at((x, y))
                    if a != 0:
                        image.set_at((x, y), (r, g, b, opacity))
        return image
    
    def shaking_animation(self, ):
        self.shake_time_left -= 1
        if self.shake_time_left <= 0:
            self.boss.rect.centerx += 5 * self.change
            self.change *= -1
            self.shake_time_left = 3

    def shaking_animation_y(self):
        self.shake_time_y_left -= 1
        if self.shake_time_y_left <= 0:
            self.boss.rect.centery += 2 * self.y_change
            self.y_change *= -1
            self.shake_time_y_left = 7