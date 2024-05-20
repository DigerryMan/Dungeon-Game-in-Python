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

    def animate(self):
        self.time -= 1
        if self.time < 0:
            self.time = self.time_cd
            self.index += 1
            self.index %= 26
            self.boss.image = self.images[self.index]
            

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