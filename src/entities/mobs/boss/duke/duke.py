import random
from config import FPS
from entities.mobs.boss.boss_health_bar import BossHealthBar
import pygame
from entities.mobs.boss.duke.duke_animation import DukeAnimation
from entities.mobs.fly_aggresive import FlyAggresive
from entities.mobs.slime import Enemy

class Duke(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self._max_health = 20
        self._health = self._max_health
        self._damage = 1

        self.health_bar = BossHealthBar(game, self)
       
        # CHANGED FROM ENEMY
        self.MOB_SIZE = int(game.settings.MOB_SIZE * 2.5)

        #SKINS
        self.image = pygame.Surface([self.MOB_SIZE, self.MOB_SIZE])

        #HITBOX
        self.rect = self.image.get_rect()
        self.rect.centerx = x * game.settings.TILE_SIZE
        self.rect.centery = y * game.settings.TILE_SIZE
        self._layer = self.rect.bottom

        #REST
        self.is_spawning_mobs = False
        self.spawning_time_cd = int(1.5 * FPS)
        self.spawning_time =  self.spawning_time_cd

        self.time_left_to_spawn_cd = int(1 * FPS)
        self.time_left_to_spawn = self.time_left_to_spawn_cd

        #MOVEMENT
        self.destination = None
        self.next_place_to_move()

        self.is_moving = False
        self.moving_time_cd = int(1.5 * FPS)
        self.moving_time = self.moving_time_cd
        #ANIMATION
        self.animation = DukeAnimation(self, game)

    def update(self):
        self.collide_player()
        self.correct_layer()
        self.animate()
        self.move()
        self.enemies_spawner()

    def enemies_spawner(self):
        if self.is_spawning_mobs:
            self.spawning_time -= 1
            if self.spawning_time <= 0:
                self.is_spawning_mobs = False
                self.spawning_time = self.spawning_time_cd
            elif self.spawning_time == self.spawning_time_cd//2:
                self.spawn_enemy()
        else:
            self.time_left_to_spawn -= 1
            if self.time_left_to_spawn <= 0:
                self.is_spawning_mobs = True
                self.time_left_to_spawn = self.time_left_to_spawn_cd
    
    def next_place_to_move(self):
        largest_x_possible, largest_y_possible = self.game.settings.MAP_WIDTH - 5, self.game.settings.MAP_HEIGHT - 5
        self.destination = random.randint(2, largest_x_possible), random.randint(2, largest_y_possible)

    def spawn_enemy(self):
        x = self.rect.centerx // self.game.settings.TILE_SIZE
        y = self.rect.centery // self.game.settings.TILE_SIZE
        room = self.game.map.get_current_room()
        x, y = self.rect.centerx//self.game.settings.TILE_SIZE, self.rect.centery//self.game.settings.TILE_SIZE
        room.spawn_mob(FlyAggresive, x, y, self)

    def animate(self):
        self.animation.animate()
    
    def draw_additional_images(self, screen):
        self.health_bar.draw(screen)
    
    def correct_layer(self):
        self._layer = self.rect.centery

    def move(self):
        if self.is_moving:
            self.move_to_destination()
        else:
            self.moving_time -= 1
            if self.moving_time <= 0:
                self.is_moving = True
                self.moving_time = self.moving_time_cd
    
    def move_to_destination(self):
        curr_x, curr_y = self.rect.left // self.game.settings.TILE_SIZE, self.rect.top // self.game.settings.TILE_SIZE
        dest_x, dest_y = self.destination
        if curr_x == dest_x and curr_y == dest_y:
            self.is_moving = False
            self.next_place_to_move()
        else:
            x_speed, y_speed = (dest_x - curr_x) * 2, (dest_y - curr_y) * 2
            self.rect.x += x_speed
            self.rect.y += y_speed
        