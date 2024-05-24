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

        self.intro_image = None
        self.intro_name = None
        self.prepare_intro_images()

        self.time = 20
        self.time_cd = 20
        self.frame_index = 0

        #SHAKING
        self.change = 1
        self.y_change = 1

        self.shake_time_left = 0
        self.shake_time_y_left = 0

        #flying
        self.index = 0

    def prepare_intro_images(self):
        img = self.img.subsurface(pygame.Rect(372, 175, 186, 166))
        self.intro_image = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))
        img = self.img.subsurface(pygame.Rect(24, 282, 138, 52))
        self.intro_name = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))

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
        elif self.boss.enemies_active:
            self.enemies_spawning_animation()
        elif self.boss.flying_active:
            self.flying_animation()
    
    def enemies_spawning_animation(self):
        frames = [0, 1]
        self.time -= 1
        self.shaking_animation()
        self.shaking_animation_y()

        if self.time <= 0:
            self.time = self.time_cd
            self.index += 1
            self.index %= 2
            self.boss.image = self.images[frames[self.index]]
            

    def laser_animation(self):
        if self.boss.lasers_time == (8 * FPS - 1):
            self.boss.image = self.change_opacity(self.images[5], 100)
            self.game.not_voulnerable.add(self.boss)
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
    
    def flying_animation(self):
        if self.boss.flying_time > int(8.7 * FPS):
            self.shaking_animation()
            self.shaking_animation_y()
            self.disappearing_animation()
        else:
            self.looped_flying_animation()

    def looped_flying_animation(self):
        frames = [2, 3, 7, 4, 10, 9, 8]
        if self.boss.flying_time % 10 == 0:
            self.index += 1
            self.index %= len(frames)
            self.boss.image = self.images[frames[self.index]]

    def disappearing_animation(self):
        if self.boss.flying_time == int(9.7 * FPS):
            self.game.not_voulnerable.add(self.boss)
            self.boss.image = self.change_opacity(self.images[5], 150)
        elif self.boss.flying_time == int(9.3 * FPS):
            self.boss.image = self.change_opacity(self.images[5], 50)
        elif self.boss.flying_time == int(8.8 * FPS):
            self.game.not_voulnerable.remove(self.boss)
            self.boss.image = self.images[5]

       