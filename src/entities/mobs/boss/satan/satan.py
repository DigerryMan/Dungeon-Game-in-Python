from cmath import cos, sin
import math
from config import FPS
from entities.bullet import Bullet
from entities.laser import Laser
from entities.mobs.boss.boss_health_bar import BossHealthBar
import pygame
from entities.mobs.boss.satan.satan_animation import SatanAnimiation
from entities.mobs.slime import Enemy
from utils.directions import Directions

class Satan(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self._max_health = 50
        self._health = self._max_health
        self._damage = 1

        self.health_bar = BossHealthBar(game, self)
        # CHANGED FROM ENEMY
        self.MOB_WIDTH = game.settings.MOB_SIZE * 5
        self.MOB_HEIGHT = game.settings.MOB_SIZE * 3

        #SKINS
        self.image = pygame.Surface([self.MOB_WIDTH, self.MOB_HEIGHT])

        #HITBOX
        self.rect = self.image.get_rect()
        self.rect.centerx = x * game.settings.TILE_SIZE
        self.rect.centery = y * game.settings.TILE_SIZE - int(self.MOB_HEIGHT * 0.4)
        self._layer = self.rect.bottom

        #ANIMATION
        self.animation = SatanAnimiation(self, game)

        # BOSS STAGES
        self.stage = 0

        # HANDS BULLETS
        self.bullets_from_hands_active = True
        self.bullets_from_hands_period = int(1 * FPS)
        self.bullets_from_hands_time = self.bullets_from_hands_period

        # LASER BREATH
        self.laser = None
        self.laser_breath_active = True
        self.laser_breath_period = int(1 * FPS)
        self.laser_breath_time = self.laser_breath_period

        # MOUTH ATTACK
        self.mouth_attack_active = True
        self.mouth_attack_period = int(1 * FPS)
        self.mouth_attack_time = self.mouth_attack_period

    def draw_additional_images(self, screen):
        self.health_bar.draw(screen)

    def animate(self):
        self.animation.animate()

    def update(self):
        self.perform_boss_stage()
        self.collide_player()
        self.correct_layer()
        self.animate()

    def perform_boss_stage(self):
        if self.bullets_from_hands_active:
            self.bullets_from_hands_time -= 1
            if self.bullets_from_hands_time == self.bullets_from_hands_period // 2:
                self.bullets_from_hands_attack()
            elif self.bullets_from_hands_time <= 0:
                self.bullets_from_hands_time = self.bullets_from_hands_period
                self.bullets_from_hands_active = False
                
        elif self.laser_breath_active:
            self.laser_breath_time -= 1
            if self.laser_breath_time == int(self.laser_breath_period * 0.75):
                self.laser_breath_attack()
            elif self.laser_breath_time == int(self.laser_breath_period * 0.42):
                self.laser.kill()
                self.laser = None
            elif self.laser_breath_time <= 0:
                self.laser_breath_time = self.laser_breath_period
                self.laser_breath_active = False
        
        elif self.mouth_attack_active:
            self.mouth_attack_time -= 1
            if self.mouth_attack_time == int(self.mouth_attack_period * 0.75):
                self.mouth_attack()
            elif self.mouth_attack_time <= 0:
                self.mouth_attack_time = self.mouth_attack_period
                #self.mouth_attack_active = False

    def mouth_attack(self):
        x, y = self.rect.centerx, self.rect.centery
        for i in range(3, 10, 3):
            Bullet(self.game, x, y, Directions.PLAYER, 10 + i, False, 1, 0.5)

    def laser_breath_attack(self):
        x, y = self.rect.centerx, self.rect.centery + int(self.MOB_HEIGHT * 0.12)
        self.laser = Laser(self.game, x, y, Directions.DOWN, False, 1, 1)

    def bullets_from_hands_attack(self):
        x, y = self.rect.centerx, self.rect.centery
        self.spawn_projectiles_in_circle(int(x + self.MOB_WIDTH * 0.35), int(y + self.MOB_HEIGHT * 0.1), True)
        self.spawn_projectiles_in_circle(int(x - self.MOB_WIDTH * 0.35), int(y + self.MOB_HEIGHT * 0.1), False)
        
    def spawn_projectiles_in_circle(self, x, y, more_to_right=False):
        bullet_velocity = 20
        angles = [x for x in range(-14, 191, 29)]
        if more_to_right:
            angles = [-alpha for alpha in angles]

        for alpha in angles:
            v_x, v_y = self.calculate_rigth_speed(bullet_velocity, alpha)
            Bullet(self.game, x, y, Directions.UP, v_y, False, 1, 0, v_x)
        

    def calculate_rigth_speed(self, v_x_y:int, alpha:int):
        v_y = v_x_y * cos(math.radians(alpha)).real
        v_x = v_x_y * sin(math.radians(-alpha)).real
        v_x_balance = abs(v_x / v_x_y) / 2
        return v_x * v_x_balance, v_y
        
    def do_to_player_jumps_stage1(self):
        self.move()
        self.attack()
    
    def start_dying(self):
        self._is_dead = True
        if self.laser is not None:
            self.laser.kill()
        self.kill()
        #self.drop_lootable()
        self.game.sound_manager.play("enemyDeath")