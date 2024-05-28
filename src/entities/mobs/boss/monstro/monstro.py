import random
from config import FPS, GREEN, WALL_MARKS
from entities.bullet import Bullet
from entities.mobs.boss.boss_health_bar import BossHealthBar
import pygame
from entities.mobs.boss.monstro.monstro_animation import MonstroAnimation
from entities.mobs.slime import Slime
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from items.stat_items.categories import Categories
from items.stat_items.item import Item
from utils.directions import Directions

class Monstro(Slime):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self._max_health = 25
        self._health = self._max_health
        self._damage = 1

        self.health_bar = BossHealthBar(game, self)
        # CHANGED FROM ENEMY
        self.MOB_SIZE = game.settings.MOB_SIZE * 2

        #SKINS
        self.image = pygame.Surface([self.MOB_SIZE, self.MOB_SIZE])

        #HITBOX
        self.rect = self.image.get_rect()
        self.rect.x = x * game.settings.TILE_SIZE
        self.rect.y = y * game.settings.TILE_SIZE
        self._layer = self.rect.bottom

        #ANIMATION
        self.animation = MonstroAnimation(self, game)

        # BOSS STAGES
        self.stage = 1

        self.is_doing_bullet_attack = False
        self.bullet_direction = None
        self.bullet_shooting_cd = 0.8 * FPS
        self.bullet_shooting_time_left = self.bullet_shooting_cd 

        self.jump_cd_s = 1
        self.jump_cd = self.jump_cd_s * FPS

        self.max_number_of_jumps = 5
        self.number_of_jumps = 0
        self.stage_1_time = None
   
    def correct_possible_jumps(self):
        self.possible_jumps.remove((0,0))

    def move(self):
        if self.is_jumping:
            self.jump()
            if not self.is_jumping:
                self.number_of_jumps += 1
        else:
            self.next_jump_time_left -= 1
            if self.next_jump_time_left <= 0:
                self.is_jumping = True
                self.jump_time_left = self.jump_time

    def find_possible_moves(self):
        x_p, y_p = self.game.player.rect.x, self.game.player.rect.y
        x, y = round(x_p / self.game.settings.TILE_SIZE), round(y_p / self.game.settings.TILE_SIZE)
       
        if x <= 0:
            x = 1
        elif x >= self.game.settings.MAP_WIDTH - 2:
            x = self.game.settings.MAP_WIDTH - 3

        if y <= 0:
            y = 1
        elif y >= self.game.settings.MAP_HEIGHT - 2:
            y = self.game.settings.MAP_HEIGHT - 3     

        self.old_jump_x, self.old_jump_y = self.new_jump_x, self.new_jump_y
        self.new_jump_x, self.new_jump_y = x, y
        if self.new_jump_x < self.old_jump_x:
            self.is_jumping_left = True
        else:
            self.is_jumping_left = False

        if abs(self.new_jump_x - self.old_jump_x) < 2:
            self.is_small_change_of_x = True
        else:
            self.is_small_change_of_x = False

        self.calculate_parabolic_jump()


    def is_valid_move(self, x, y):
        if x <= 0 or x >= self.game.settings.MAP_WIDTH - 2 or y <= 0  or y >= self.game.settings.MAP_HEIGHT - 2:

            return False
        return self.room_layout[y][x] not in WALL_MARKS    

    def calculate_parabolic_jump(self):
        self.z = self.new_jump_x - self.old_jump_x
        self.v_x = self.z / (self.t)
        if self.v_x == 0:
            self.tg = None
            self.v_y = (self.new_jump_y - self.old_jump_y) / (self.t)
        else:
            self.tg = ((self.new_jump_y - self.old_jump_y) - 0.5 * 9.81 * (self.t) ** 2) / (self.v_x * (self.t))

    def calculate_current_y(self, t:float):
        if self.new_jump_x == self.old_jump_x and self.old_jump_y == self.new_jump_y:
            return self.old_jump_y
        if self.tg == None:
            return self.old_jump_y + t * self.v_y
        return self.old_jump_y + self.v_x * t * self.tg + 0.5 * 9.81 * t ** 2

    def update(self):
        self.perform_boss_stage()

        self.collide_player()
        self.correct_layer()
        self.animate()

    def animate(self):
        self.animation.animate()
    
    def perform_boss_stage(self):
        if self.stage == 1:
            if self.number_of_jumps >= self.max_number_of_jumps:
                self.stage = 0  
                self.animation.idles_passed = 0
                self.number_of_jumps = 0
                self.roll_next_jumps_amount()
            else:
                self.do_to_player_jumps_stage1()
        
        elif self.stage == 0:
            self.do_bullet_attack_stage0()
            self.is_doing_bullet_attack = True

    def roll_next_jumps_amount(self):
        self.max_number_of_jumps = random.randint(1, 3)

    def draw_additional_images(self, screen):
        self.health_bar.draw(screen)

    def do_bullet_attack_stage0(self):
        self.bullet_shooting_time_left -= 1
        if self.bullet_shooting_time_left == int(self.bullet_shooting_cd * 0.6):
            self.shoot_one_of_crazy_bullets()
            
        elif self.bullet_shooting_time_left <= 0:
            self.bullet_shooting_time_left = self.bullet_shooting_cd
            self.stage = 1
            self.is_doing_bullet_attack = False

    def update_bullet_direction(self):
        x_p, y_p = self.game.player.get_center_position()
        self.bullet_direction = Directions.get_direction_from_two_points(self.rect.centerx, self.rect.centery, x_p, y_p) 

    def shoot_one_of_crazy_bullets(self):
        self.update_bullet_direction()
        for i in range(9):
            x, y = self.rect.centerx + random.randint(-12, 12), self.rect.centery + random.randint(-12, 12)
            decay = random.random() * 0.2 + 0.3
            speed = random.randint(15, 25) 

            additional_speed = random.randint(-4, 4) 
            Bullet(self.game, x, y, self.bullet_direction, speed, 
                False, self._damage, decay, additional_speed)
                
        self.game.sound_manager.play(f"tear{random.randint(1, 2)}")
        

    def do_to_player_jumps_stage1(self):
        self.move()
        self.attack()

    def drop_lootable(self):
        for _ in range(5):
            self.room.items.append(SilverCoin(self.game, self.rect.centerx, self.rect.centery))

        for _ in range(3):
            self.room.items.append(GoldenCoin(self.game, self.rect.centerx, self.rect.centery))

        for _ in range(2):
            self.room.items.append(PickupHeart(self.game, self.rect.centerx, self.rect.centery))

        self.room.items.append(Item(self.game, self.rect.centerx, self.rect.centery, Categories.LEGENDARY, drop_animation=True, boss="monstro"))