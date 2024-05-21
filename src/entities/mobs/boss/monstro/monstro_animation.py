import pygame
from config import FPS

class MonstroAnimation():
    def __init__(self, boss, game):
        self.boss = boss
        self.game = game
        self.img = game.image_loader.bosses["monstro"]
        self.images = []
        self.prepare_images()
        self.boss.image = self.images[2]
        self.boss.mask = pygame.mask.from_surface(self.boss.image)

        #IDLE
        self.idle_time_left = (0.2 * FPS)
        self.idle_frame = 1
        self.idles_passed = 0
        
        #JUMP
        self.jumps_order = [5, 6, 7, 4, 5, 8]
        self.list_of_jumpers = [1, 0.9, 0.75, 0.3, 0.1, 0.06]
        self.list_of_jumpers = [int(t * self.boss.jump_time) for t in self.list_of_jumpers]
        self.jump_index = 0

    def prepare_images(self):
        for y in range(2):
            for x in range(5):
                image = self.img.subsurface(pygame.Rect(x * 80, y * 112 + 36, 80, 112 - 36))
                self.images.append(pygame.transform.scale(image, (self.boss.MOB_SIZE, self.boss.MOB_SIZE)))

    def animate(self):
        if self.boss.stage == 1:
            if self.idles_passed < 4 and not self.boss.is_jumping:
                self.idle_anime(int(self.boss.jump_cd * 0.2))
            elif self.boss.number_of_jumps <= self.boss.max_number_of_jumps and self.boss.is_jumping:
                self.jumping_anime()
                self.idle_time_left = 0
        else:
            if self.boss.bullet_shooting_time_left < int(self.boss.bullet_shooting_cd * 0.4):
                self.idle_anime(int(self.boss.bullet_shooting_cd * 0.35 * 2))
            if self.boss.bullet_shooting_time_left == int(self.boss.bullet_shooting_cd * 0.8):
                self.bullet_shoot_anime()
                self.idle_time_left = 0

    def bullet_shoot_anime(self):
        self.boss.image = self.image_rotator(self.images[3])
        self.boss.mask = pygame.mask.from_surface(self.boss.image)

    def idle_anime(self, time):
        self.idle_time_left -= 1
        if self.idle_time_left <= 0:
            self.idles_passed += 1
            self.idle_frame = 1 + self.idle_frame % 2
            self.idle_time_left = time
            self.boss.image = self.image_rotator(self.images[self.idle_frame])
            self.boss.mask = pygame.mask.from_surface(self.boss.image)
    
    def jumping_anime(self):
        if int(self.boss.jump_time_left) in self.list_of_jumpers:
            self.boss.image = self.image_rotator(self.images[self.jumps_order[self.jump_index]])
            self.boss.mask = pygame.mask.from_surface(self.boss.image)
            self.jump_index += 1
            self.jump_index %= len(self.jumps_order) 
            self.idles_passed = 0
    
    def image_rotator(self, image):
        if self.game.player.rect.centerx > self.boss.rect.centerx:
            return pygame.transform.flip(image, True, False)
        return image
