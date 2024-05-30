from config import FPS
from entities.laser import Laser
from entities.mobs.boss.boss_health_bar import BossHealthBar
import pygame
from entities.mobs.boss.forsaken.forsaken_animation import ForsakenAnimation
from entities.mobs.legs import Legs
from entities.mobs.slime import Enemy
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from items.stat_items.categories import Categories
from items.stat_items.item import Item
from utils.directions import Directions
from utils.image_transformer import ImageTransformer

class Forsaken(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self.size = "Large"
        self._max_health = 60
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

        # LASERS
        self.lasers_active = True
        self.laser_cd = 8 * FPS
        self.lasers_time = self.laser_cd
       
        # ENEMIES SPAWN
        self.enemies_active = False
        self.enemies_cd = 5 * FPS
        self.enemies_time = self.enemies_cd

        # FLYING
        self.flying_active = False
        self.flying_cd = 10 * FPS
        self.flying_time = self.flying_cd

        self.y_speed = int(18 * self.game.settings.SCALE)
        self.x_speed = int(8 * self.game.settings.SCALE)
        self.y_multiplier = -1

        self.changes_made = 0
        self.respect_collisions = False

    def update(self):
        self.collide_player()
        self.correct_layer()
        if self.hit_time > 0:
            self.hit_time -= 1
            if self.hit_time == 0:
                self.restore_image_colors()

        self.is_change_of_frame = False
        self.animate()
        if self.is_change_of_frame and self.hit_time > 0:
            self.image = ImageTransformer.change_image_to_more_red(self.unchanged_image)
        
        self.boss_stages()

    def boss_stages(self):
        if self.lasers_active:
            self.laser_spawner()
        elif self.enemies_active:
            self.enemies_spawner()
        elif self.flying_active:
            self.flying()

    def laser_spawner(self):
        self.lasers_time -= 1
        if self.lasers_time == int(7.99* FPS):
            self.play_audio("forsakenLaser")
        elif self.lasers_time == int(6.5* FPS):
            self.spawn_lasers_horizontally()
        elif self.lasers_time == int(4.5 * FPS):
            self.spawn_lasers_vertically()
        elif self.lasers_time == int(1.5 * FPS):
            self.spawn_lasers_horizontally()
            self.spawn_lasers_vertically()
        elif self.lasers_time <= 0:
            self.lasers_active = False
            self.flying_active = True
            self.lasers_time = self.laser_cd
            self.game.not_voulnerable.remove(self)

        self.playing_delayed_laser_sound()

    def playing_delayed_laser_sound(self):
        if self.lasers_time in [int(6.3* FPS), int(4.3* FPS), int(1.3* FPS)]:
            Laser.play_audio(self.game.sound_manager)

    def enemies_spawner(self):
        self.enemies_time -= 1
        if self.enemies_time <= 0:
            self.enemies_active = False
            self.enemies_time = self.enemies_cd
            self.lasers_active = True
        elif self.enemies_time == int(4.5 * FPS) or self.enemies_time == int(3.5 * FPS):
            self.play_audio("forsakenSpawn")
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
            Laser(self.game, new_x, new_y, Directions.DOWN, False, 1, duration, opacity_time, audio_on=False)
    
    def spawn_lasers_vertically(self, duration=1.5, opacity_time=0.4):
        self.lasers_active = True
        tile_size = self.game.settings.TILE_SIZE
        for y in range(2, self.game.settings.MAP_HEIGHT, 2):
            new_x =tile_size
            new_y = y * tile_size 
            Laser(self.game, new_x, new_y, Directions.RIGHT, False, 1, duration, opacity_time, audio_on=False)
    
    def flying(self):
        self.flying_time -= 1
        if self.flying_time == int(8.8 * FPS):
            self.play_audio("forsakenRoar")
        
        if self.flying_time == int(9 * FPS):
            self.setup_start_of_fly()
        
        elif self.flying_time <= 0:
            self.play_audio("forsakenRoar")
            self.flying_active = False
            self.flying_time = self.flying_cd
            self.respect_collisions = False
            self.enemies_active = True
            self.changes_made = 0
            self.y_multiplier = -1
        
        elif self.flying_time < int(8 * FPS):
            self.fly()
           
    def setup_start_of_fly(self):        
        tile_size = self.game.settings.TILE_SIZE
        self.rect.centery = (self.game.settings.MAP_HEIGHT - 3/2) * tile_size
        self.rect.centerx = int(3 * tile_size / 2)
    
    def fly(self):
        self.block_collision_detection()
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed * self.y_multiplier


    def block_collision_detection(self):
        rect_hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if rect_hits:
            mask_hits = self.get_mask_colliding_sprite(rect_hits)
            if mask_hits and self.respect_collisions:
                self.play_audio("forsakenRockHit")
                self.changes_made += 1
                self.y_multiplier *= -1
                if self.changes_made == 6:
                    self.x_speed *= -1
                    self.changes_made = 0
        elif self.rect.centery < self.game.settings.WIN_HEIGHT // 2:
            self.respect_collisions = True

    def drop_lootable(self):
        drops = [SilverCoin] * 15 + [GoldenCoin] * 10 + [PickupHeart] * 3
        for drop in drops:
            self.room.items.append(drop(self.game, self.rect.centerx, self.rect.centery))
        
        self.room.items.append(Item(self.game, self.rect.centerx, self.rect.centery, Categories.LEGENDARY, boss="forsaken"))