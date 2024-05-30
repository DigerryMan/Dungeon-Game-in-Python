import random
import pygame
from config import FPS, WALL_MARKS
from entities.bullet import Bullet
from entities.enemy import Enemy
from utils.directions import Directions

class Slime(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, check_block_colisions=False, 
                         is_wandering=False, bullet_decay_sec=3)

        #CHANGEABLE STATS
        self._health = 6
        self._projectal_speed = 6
        
        self.t = random.random() * 0.5 + 0.8 #time of jump in sec
        self.jump_time = int(self.t * FPS) 
        self.jump_cd = int((random.random() * 0.8 + 1.2) * FPS)
        self.jump_range = 3 # has to be min 2

        #SKINS
        self.img = game.image_loader.get_image('slime')
        self.img_shadow = game.image_loader.get_image('slime_shadow')
        self.img_shadow = pygame.transform.scale(self.img_shadow, (int(self.MOB_SIZE * 0.6), int(self.MOB_SIZE * 0.6)))

        self.prepare_images()
        self.image = self.images[0]
        self.unchanged_image = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.frame_x = 0
        self.frame_y = 0

        self.animation_jump_time = [0.25, 0.15, 0.05]       # <0.3
        self.animation_afk_time = [0.65, 0.5, 0.35]         # >=0.3 & <=0.7
        self.animation_land_time = [0.99, 0.94, 0.89, 0.84] # >0.7 
        self.prepare_animation_time()
        self.v_shadow_y = 0

        #POSITION
        self.x = x
        self.y = y
        
        #MOVES
        self.room_layout = self.game.map.get_current_room().get_block_layout()
        self.possible_jumps = [(x_i, y_j) for x_i in range(-self.jump_range, self.jump_range + 1) 
                               for y_j in range(-self.jump_range, self.jump_range + 1)]
        self.correct_possible_jumps()

        #JUMPING
        self.is_jumping = False
        self.jump_time_left = 0
        self.next_jump_time_left = int(0.7 * self.jump_cd) #START FOR ANIMATION
        self.is_jumping_left = False
        self.is_small_change_of_x = False

        self.new_jump_x = x
        self.new_jump_y = y
        self.old_jump_x = x
        self.old_jump_y = y

        #FOR Y CALCULATIONS
        self.z = 0
        self.v_x = 0
        self.tg = 0

        #REST
        self.find_possible_moves() #for first animation to work
        self.shadow_y = y * game.settings.TILE_SIZE
        self.shadow_x = x * game.settings.TILE_SIZE
        self.prepare_atack = False

    def prepare_images(self):
        for y in range(3):
            for x in range(4):
                self.images.append(self.img.subsurface(pygame.Rect(x * self.MOB_SIZE, y * self.MOB_SIZE, self.MOB_SIZE, self.MOB_SIZE)))

    def prepare_animation_time(self):
        for index, value in enumerate(self.animation_jump_time):
            self.animation_jump_time[index] = int(value * self.jump_cd)
        
        for index, value in enumerate(self.animation_afk_time):
            self.animation_afk_time[index] = int(value * self.jump_cd)
        
        for index, value in enumerate(self.animation_land_time):
            self.animation_land_time[index] = int(value * self.jump_cd)

    def correct_possible_jumps(self):
        self.possible_jumps.remove((0, 0))
         #remove diagonal jumps
        for y in range(1, self.jump_range + 1):
            self.possible_jumps.remove((0, y))
            self.possible_jumps.remove((0, -y))
        
         #remove 1 block jumps
        for y in range(-1, 2):
            self.possible_jumps.remove((-1, y))
            self.possible_jumps.remove((1, y))

    def move(self):
        if self.is_jumping:
            self.jump()
        else:
            self.next_jump_time_left -= 1
            if self.next_jump_time_left <= 0:
                self.is_jumping = True
                self.jump_time_left = self.jump_time
    
    def jump(self):
        self.jump_time_left -= 1
        if self.jump_time_left <= 0: #end of jump
            self.play_audio("monstroLand")
            self.x = self.new_jump_x
            self.y = self.new_jump_y
            self.rect.x = self.new_jump_x * self.game.settings.TILE_SIZE
            self.rect.y = self.new_jump_y * self.game.settings.TILE_SIZE

            self.find_possible_moves()
            self.next_jump_time_left = self.jump_cd            
            self.is_jumping = False
            self.prepare_atack = True

        else: #jump
            if self.jump_time_left == self.jump_cd - 1:
                self.play_audio("monstroJump")
            elapsed_time_sec = (self.jump_time - self.jump_time_left) / FPS
            y = self.calculate_current_y(elapsed_time_sec)
            x = self.old_jump_x + self.v_x * elapsed_time_sec
            self.rect.x = int(x * self.game.settings.TILE_SIZE) 
            self.rect.y = int(y * self.game.settings.TILE_SIZE)

            #FOR SHADOW DISPLAY
            self.shadow_y = int((self.old_jump_y + self.v_shadow_y * elapsed_time_sec) * self.game.settings.TILE_SIZE)
            self.shadow_x = self.rect.x

    def find_possible_moves(self):
        possible_moves = []
        for jump in self.possible_jumps:
            new_x = self.x + jump[0] 
            new_y = self.y + jump[1]
            if self.is_valid_move(new_x, new_y):
                possible_moves.append((new_x, new_y))
        
        if possible_moves:
            self.old_jump_x, self.old_jump_y = self.new_jump_x, self.new_jump_y
            self.new_jump_x, self.new_jump_y = random.choice(possible_moves)
            if self.new_jump_x < self.old_jump_x:
                self.is_jumping_left = True
            else:
                self.is_jumping_left = False

            if abs(self.new_jump_x - self.old_jump_x) < 2:
                self.is_small_change_of_x = True
            else:
                self.is_small_change_of_x = False

            self.calculate_parabolic_jump()
        
    def calculate_parabolic_jump(self):
        self.z = self.new_jump_x - self.old_jump_x
        self.v_x = self.z / (self.t)
        self.v_shadow_y = (self.new_jump_y - self.old_jump_y) / self.t
        self.tg = ((self.new_jump_y - self.old_jump_y) - 0.5 * 9.81 * (self.t) ** 2) / (self.v_x * (self.t))

    def calculate_current_y(self, t:float):
        return self.old_jump_y + self.v_x * t * self.tg + 0.5 * 9.81 * t ** 2

    def is_valid_move(self, x, y):
        if x <= 0 or x >= self.game.settings.MAP_WIDTH - 1 or y <= 0  or y >= self.game.settings.MAP_HEIGHT - 1:
            return False
        return self.room_layout[y][x] not in WALL_MARKS

    def attack(self):
        if self.prepare_atack:
            self.prepare_atack = False
            direction_to_shoot = Directions.LEFT
            for _ in range(4):
                Bullet(self.game, self.rect.centerx, self.rect.centery, direction_to_shoot, 
                    speed=self._projectal_speed, is_friendly=False, dmg=1, 
                    time_decay_in_seconds=self._bullet_decay_sec)
                direction_to_shoot = direction_to_shoot.rotate_clockwise()
    
    def correct_layer(self):
        if self.is_jumping:
            self._layer = self.rect.bottom + 2500
        else:
            self._layer = self.rect.bottom
    
    def animate(self):
        if not self.is_jumping:
            unconvention_change = False

            if self.next_jump_time_left > int(0.7 * self.jump_cd): #landing
                if self.next_jump_time_left in self.animation_land_time:
                    self.change_of_frame()

            elif self.next_jump_time_left < int(0.3 * self.jump_cd): #jumping
                if self.next_jump_time_left in self.animation_jump_time:
                    if self.next_jump_time_left == self.animation_jump_time[-1] and self.is_small_change_of_x:
                        self.change_of_frame(self.is_small_change_of_x)
                        unconvention_change = True
                        self.is_small_change_of_x = False
                    else:
                        self.change_of_frame()
            
            else: #afk 
                if self.next_jump_time_left in self.animation_afk_time:
                    self.change_of_frame()
                    if self.frame_x > 1:
                        self.frame_x = 0

            if self.frame_x > 3:
                self.frame_x = 0
                self.frame_y += 1
            if self.frame_y > 1:
                self.frame_y = 0 

            if self.is_change_of_frame:
                self.frame = self.images[self.frame_x + self.frame_y * 4]
                if self.is_jumping_left and self.next_jump_time_left < int(0.3 * self.jump_cd):
                    self.frame = pygame.transform.flip(self.frame, True, False)
   
                self.image = self.frame
                self.unchanged_images = self.frame
                self.mask = pygame.mask.from_surface(self.image)

                if unconvention_change:
                    self.frame_x = 0
                    self.frame_y = 1

    def change_of_frame(self, unconvention_change=False):
        self.is_change_of_frame = True
        if not unconvention_change:
            self.frame_x += 1
        else:
            self.frame_x = 0
            self.frame_y = 0
        
    def draw_additional_images(self, screen):
        self.draw_shadow(screen)
    
    def draw_shadow(self, screen):
        if self.is_jumping:
            screen.blit(self.img_shadow, (self.shadow_x + self.MOB_SIZE//4, self.shadow_y + self.MOB_SIZE//2))