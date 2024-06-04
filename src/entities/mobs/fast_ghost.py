import pygame
from entities.mobs.ghost import Ghost

class FastGhost(Ghost):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self._health = 3
        self._speed = 4 * game.settings.SCALE
        self._projectal_speed = 9

        self.images = []
        self.img = game.image_loader.mobs["fast_ghost"]
        self.__prepare_images()
    
    def __prepare_images(self):
        for y in range(3):
            for x in range(4):
                img_help = self.img.subsurface(pygame.Rect(x * 48, y * 48, 48, 48))
                self.images.append(pygame.transform.scale(img_help, (self.MOB_SIZE, self.MOB_SIZE)))
    