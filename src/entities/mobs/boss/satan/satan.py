from config import FPS, GREEN
from entities.mobs.boss.boss_health_bar import BossHealthBar
import pygame
from entities.mobs.boss.satan.satan_animation import SatanAnimiation
from entities.mobs.slime import Enemy

class Satan(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self._max_health = 50
        self._health = self._max_health
        self._damage = 1

        self.health_bar = BossHealthBar(game, self)
        # CHANGED FROM ENEMY
        self.MOB_WIDTH = game.settings.MOB_SIZE * 3.2
        self.MOB_HEIGHT = game.settings.MOB_SIZE * 2.5

        #SKINS
        self.image = pygame.Surface([self.MOB_WIDTH, self.MOB_HEIGHT])

        #HITBOX
        self.rect = self.image.get_rect()
        self.rect.x = x * game.settings.TILE_SIZE
        self.rect.y = y * game.settings.TILE_SIZE
        self._layer = self.rect.bottom

        #ANIMATION
        self.animation = SatanAnimiation(self, game)

        # BOSS STAGES
        self.stage = 1

        self.bullet_direction = None
        self.bullet_shooting_cd = 0.8 * FPS
        self.bullet_shooting_time_left = self.bullet_shooting_cd 

        self.jump_cd_s = 0.4
        self.jump_cd = self.jump_cd_s * FPS

        self.max_number_of_jumps = 5
        self.number_of_jumps = 0
        self.stage_1_time = None
        
 
    
    def update(self):
        self.perform_boss_stage()

        self.collide_player()
        self.correct_layer()
        self.animate()

    def animate(self):
        self.animation.animate()
    
    def perform_boss_stage(self):
        if self.stage == 1:
            if self.number_of_jumps > self.max_number_of_jumps:
                self.stage = 0  
                self.number_of_jumps = 0
                self.roll_next_jumps_amount()
            else:
                self.do_to_player_jumps_stage1()
        
        elif self.stage == 0:
            self.do_bullet_attack_stage0()

    def draw_additional_images(self, screen):
        self.health_bar.draw(screen)

    def do_bullet_attack_stage0(self):
        self.bullet_shooting_time_left -= 1
        if self.bullet_shooting_time_left <= 0:
            self.shoot_one_of_crazy_bullets()
            self.bullet_shooting_time_left = self.bullet_shooting_cd
            self.stage = 1

    def do_to_player_jumps_stage1(self):
        self.move()
        self.attack()