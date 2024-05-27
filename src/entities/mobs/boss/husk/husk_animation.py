import pygame
from entities.mobs.boss.duke.duke_animation import DukeAnimation

class HuskAnimation(DukeAnimation):
    def __init__(self, boss, game):
        super().__init__(boss, game)
        self.images = []
        self.prepare_images()

        self.intro_image = None
        self.intro_name = None
        self.prepare_intro_images()

    def prepare_intro_images(self):
        img = self.img.subsurface(pygame.Rect(45, 389, 116, 116))
        self.intro_image = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))
        
        img = self.img.subsurface(pygame.Rect(220, 414, 100, 51))
        self.intro_name = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))

    def prepare_images(self):
        for y in range(2):
            for x in range(2, 4):
                image = self.img.subsurface(pygame.Rect(x * 80 + 30, y * 64, 80, 64))
                self.images.append(pygame.transform.scale(image, (self.boss.MOB_SIZE, self.boss.MOB_SIZE)))
