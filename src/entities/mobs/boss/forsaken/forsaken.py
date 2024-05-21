import random
from config import FPS, WALL_MARKS
from entities.laser import Laser
from entities.mobs.boss.boss_health_bar import BossHealthBar
import pygame
from entities.mobs.boss.forsaken.forsaken_animation import ForsakenAnimation
from entities.mobs.legs import Legs
from entities.mobs.slime import Enemy
from utils.directions import Directions

class Forsaken(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self._max_health = 35
        self._health = self._max_health
        self._damage = 1

        self.health_bar = BossHealthBar(game, self)
        # CHANGED FROM ENEMY
        self.MOB_SIZE = int(game.settings.MOB_SIZE * 3.5)

        #SKINS
        self.image = pygame.Surface([self.MOB_SIZE, self.MOB_SIZE])

        #HITBOX
        self.rect = self.image.get_rect()
        self.rect.centerx = x * game.settings.TILE_SIZE
        self.rect.centery = y * game.settings.TILE_SIZE
        self._layer = self.rect.bottom

        #ANIMATION
        self.animation = ForsakenAnimation(self, game)

        # BOSS STAGES
        self.lasers_active = True
        self.laser_cd = 8 * FPS
        self.lasers_time = self.laser_cd
       
        # ENEMIES SPAWN
        self.enemies_active = True
        self.enemies_cd = 5 * FPS
        self.enemies_time = self.enemies_cd

    def update(self):
        self.collide_player()
        self.correct_layer()
        self.animate()
        self.boss_stages()

    def boss_stages(self):
        if self.lasers_active:
            self.laser_spawner()
        elif self.enemies_active:
            self.enemies_spawner()

    def laser_spawner(self):
        self.lasers_time -= 1
        if self.lasers_time == int(6.5* FPS):
            self.spawn_lasers_horizontally()
        elif self.lasers_time == int(4.5 * FPS):
            self.spawn_lasers_vertically()
        elif self.lasers_time == int(1.5 * FPS):
            self.spawn_lasers_horizontally()
            self.spawn_lasers_vertically()
        elif self.lasers_time <= 0:
            self.lasers_active = False
            self.enemies_active = True
            self.lasers_time = self.laser_cd

    def enemies_spawner(self):
        self.enemies_time -= 1
        if self.enemies_time <= 0:
            self.enemies_active = False
            self.enemies_time = self.enemies_cd
            self.lasers_active = True
        elif self.enemies_time == int(4.5 * FPS) or self.enemies_time == int(3.8 * FPS):
            self.game.map.get_current_room().spawn_mob(Legs, self.rect.centerx//self.game.settings.TILE_SIZE, self.rect.centery//self.game.settings.TILE_SIZE)

    def animate(self):
        self.animation.animate()
    
    def draw_additional_images(self, screen):
        self.health_bar.draw(screen)
    
    def spawn_lasers_horizontally(self, duration=1.5, opacity_time=0.4):
        self.lasers_active = True
        tile_size = self.game.settings.TILE_SIZE
        for x in range(3, self.game.settings.MAP_WIDTH - 1, 2):
            new_x = x * tile_size + tile_size // 12
            new_y = tile_size
            Laser(self.game, new_x, new_y, Directions.DOWN, False, 1, duration, opacity_time)
    
    def spawn_lasers_vertically(self, duration=1.5, opacity_time=0.4):
        self.lasers_active = True
        tile_size = self.game.settings.TILE_SIZE
        for y in range(2, self.game.settings.MAP_HEIGHT, 2):
            new_x =tile_size
            new_y = y * tile_size 
            Laser(self.game, new_x, new_y, Directions.RIGHT, False, 1, duration, opacity_time)
    
