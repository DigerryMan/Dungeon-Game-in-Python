import pygame
from entities.mobs.boss.boss_health_bar import BossHealthBar
from entities.mobs.boss.duke.duke import Duke
from entities.mobs.boss.husk.husk_animation import HuskAnimation

class Husk(Duke):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self._max_health = 50
        self._health = self._max_health
        self._damage = 1.5
        
        self.health_bar = BossHealthBar(game, self)

        #SKINS
        self.animation = HuskAnimation(self, game)