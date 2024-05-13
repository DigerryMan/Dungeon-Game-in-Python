from config import GREEN
from entities.enemy import Enemy
from entities.mobs.boss.boss_health_bar import BossHealthBar
import pygame

class Boss(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self._max_health = 25
        self._health = self._max_health

        self.health_bar = BossHealthBar(game, self)
        self.image = game.image_loader.get_image("parasite").subsurface(pygame.Rect(0, 0, self.MOB_SIZE, self.MOB_SIZE)).copy()
        self.image.fill(GREEN)

    def animate(self):
        pass

    def draw_additional_images(self, screen):
        self.health_bar.draw(screen)