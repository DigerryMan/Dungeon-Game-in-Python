import pygame
from config import *
from entities.bomb import Bomb
from entities.mobs.friendly_ghost import FriendlyGhost
from entities.player.equipment import Equipment
from entities.player.stat_bars import StatBars
from items.item_types import ItemType
from utils.directions import Directions
from ..bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        #MAIN
        self.game = game
        self.max_health = BASE_HEALTH
        self.health = BASE_HEALTH
        self.speed = BASE_SPEED * game.settings.SCALE
        self.PLAYER_SIZE = game.settings.PLAYER_SIZE
        self.coins = 0
        #self.bombs = 0
        self.bombs = 10
        self.rooms_cleared = 0

        #SKIN
        self.img = game.image_loader.get_image("player")
        self.body_images = []
        self.head_images = []
        self.prepare_images()
        self.frame = None
        self.image = self.body_images[0]

        #HITBOX / POSITION
        self.rect = self.image.get_rect()
        self.rect.x = x * self.PLAYER_SIZE
        self.rect.y = y * self.PLAYER_SIZE
        self.x_change = 0
        self.y_change = 0
        self.is_moving = False

        #DIRECTION
        self.facing = Directions.DOWN
        self.direction = Directions.DOWN
        self.last_horizontall_facing = Directions.RIGHT

        #EQ
        self.eq = Equipment(self)
        self.eq_opened = False

        #ANIMATION
        self.x_legs_frame = 0
        self.body_frame = None
        self.reversed_body_frame = False
        self.x_head_frame = 0
        self.head_frame = None
        self.reversed_head = False
        self.head_tear_anime_cd = 4
        self.head_tear_anime_time_left = -1
        
        self.next_frame_ticks_cd = 3
        self.time = 0
        self._layer = self.rect.bottom
        
        #SHOOTING
        self.shot_time_left = 0
        self.shot_try = False

        #SECOND SHOOT
        self.shoot_second_bullet = False
        self.shoot_second_time = 0

        #DEATH ANIMATION
        self.is_alive = True
        self.end_of_death_animation = False
        self.death_frame_cd = 12
        self.death_time_left = self.death_frame_cd
        self.death_index = 0
        self.last_death_index = 4

        #REST
        self.immortality_time_left = 0

        self.groups = self.game.all_sprites, self.game.player_sprite, self.game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animate()
        self.mask = pygame.mask.from_surface(self.image)
        self.correct_player_mask()
        
    def prepare_images(self):
        for y in range(1, 3):
            for x in range(10):
                self.body_images.append(self.img.subsurface(pygame.Rect(x * self.PLAYER_SIZE, y * self.PLAYER_SIZE, self.PLAYER_SIZE, self.PLAYER_SIZE)))

        for x in range(6):
            self.head_images.append(self.img.subsurface(pygame.Rect(x * self.PLAYER_SIZE, 0, self.PLAYER_SIZE, self.PLAYER_SIZE)))

    def correct_player_mask(self):
        removed_hitbox_from_sides = pygame.Surface((self.mask.get_size()[0] * 0.25, self.mask.get_size()[1]))
        removed_hitbox_from_top = pygame.Surface((self.mask.get_size()[0], self.mask.get_size()[1] * 0.25))
        cut_mask_sides = pygame.mask.from_surface(removed_hitbox_from_sides)
        cut_mask_top = pygame.mask.from_surface(removed_hitbox_from_top)

        self.mask.erase(cut_mask_sides, (0, 0))
        self.mask.erase(cut_mask_sides, (self.mask.get_size()[0] - cut_mask_sides.get_size()[0], 0))
        self.mask.erase(cut_mask_top, (0, 0))

    def update(self):
        if self.is_alive:
            self.user_input()
            self.correct_diagonal_movement()

            self.rect.x += self.x_change
            self.collide_blocks('x')
            self.rect.y += self.y_change
            self.collide_blocks('y')

            self.check_items_pick_up()
            self._layer = self.rect.bottom
            self.animate()

            self.immortality_time_left -= 1
            self.x_change = 0
            self.y_change = 0
        else:
            if not self.end_of_death_animation:
                self.play_death_animation() 
            else:
                self.game.game_over()

    def user_input(self):
        keys = pygame.key.get_pressed()
        x_y_vel = [0,0]
        self.is_moving = False
        self.move(keys, x_y_vel)
        self.plant_bomb(x_y_vel)
        self.shoot(keys, x_y_vel)

    def move(self, keys, x_y_vel):
        if keys[pygame.K_a]:
            self.x_change -= int(self.speed)
            self.facing = Directions.LEFT
            self.direction = Directions.LEFT
            self.last_horizontall_facing = Directions.LEFT
            x_y_vel[0] -= 1
            self.is_moving = True
        
        if keys[pygame.K_d]:
            self.x_change += int(self.speed)
            self.facing = Directions.RIGHT
            self.direction = Directions.RIGHT
            self.last_horizontall_facing = Directions.RIGHT
            x_y_vel[0] += 1
            self.is_moving = True

        if keys[pygame.K_w]: 
            self.y_change -= int(self.speed)
            self.facing = Directions.UP
            self.direction = Directions.UP
            x_y_vel[1] -= 1
            self.is_moving = True

        if keys[pygame.K_s]:
            self.y_change += int(self.speed)
            self.facing = Directions.DOWN
            self.direction = Directions.DOWN
            x_y_vel[1] += 1
            self.is_moving = True

    def plant_bomb(self, x_y_vel):
        if self.game.e_pressed and self.bombs > 0:
            if self.facing == Directions.LEFT or x_y_vel[0] < 0:
                Bomb(self.game, self.rect.centerx, self.rect.centery, rotate = True)
            else:
                Bomb(self.game, self.rect.centerx, self.rect.centery)
            self.bombs -= 1

    def shoot(self, keys, x_y_vel):
        self.shot_time_left -= 1
        self.shoot_second_bullet -= 1
        self.shot_try = False

        key_to_direction = {
            pygame.K_LEFT: Directions.LEFT,
            pygame.K_RIGHT: Directions.RIGHT,
            pygame.K_UP: Directions.UP,
            pygame.K_DOWN: Directions.DOWN
        }

        for key, direction in key_to_direction.items():
            if keys[key]:
                self.facing = direction
                self.shot_try = True
            
        if self.shot_try or self.shoot_second_bullet >= 0:
            if self.shot_time_left <= 0:
                self.shot_time_left = self.get_shooting_cooldown() 
                if self.eq.extra_stats["extra_shot_time"]:
                    self.shoot_second_bullet = self.eq.extra_stats["extra_shot_time"]
                self.shoot_one_bullet(x_y_vel)

            elif self.shoot_second_bullet == 0:
                self.shoot_one_bullet(x_y_vel)
                self.shot_time_left = self.get_shooting_cooldown()
            else:
                self.shot_try = False

    def shoot_one_bullet(self, x_y_vel):
        additional_v = 0
        if PLAYER_SHOOT_DIAGONAL:
            _, other_axis_index = self.facing.rotate_clockwise().get_axis_tuple()     
            if x_y_vel[other_axis_index]:
                additional_v = int(self.get_shot_speed() * x_y_vel[other_axis_index] * DIAGONAL_MULTIPLIER) 

        x, y = self.calculate_bullet_position()
        self.head_tear_anime_time_left = self.head_tear_anime_cd
        Bullet(self.game, x, y, self.facing, self.get_shot_speed(), True,
                (BASE_DMG+self.eq.stats["dmg"])*self.eq.extra_stats["dmg_multiplier"], BASE_BULLET_FLY_TIME+self.eq.stats["bullet_fly_time"],
                additional_speed=additional_v)  
        
    def calculate_bullet_position(self):
        x, y = self.rect.centerx, self.rect.centery
        if self.facing == Directions.LEFT:
            x -= self.PLAYER_SIZE//2
        elif self.facing == Directions.RIGHT:
            x += self.PLAYER_SIZE//2
        elif self.facing == Directions.UP:
            y -= self.PLAYER_SIZE//2
        elif self.facing == Directions.DOWN:
            y += self.PLAYER_SIZE//2
        return x, y

    def correct_diagonal_movement(self):
        if(self.x_change and self.y_change):
            self.x_change //= 1.41
            self.y_change //= 1.41
            if self.x_change < 0:
                self.x_change += 1
            if self.y_change < 0:
                self.y_change += 1
                
    def collide_blocks(self, direction:str):
        rect_hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if rect_hits:
            mask_hits = self.get_mask_colliding_sprite(rect_hits)
            if mask_hits: 
                if direction == 'x':
                    self.rect.x -= self.x_change
                elif direction == 'y':
                    self.rect.y -= self.y_change

    def get_mask_colliding_sprite(self, rect_hits):
        for sprite in rect_hits:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite

    def check_items_pick_up(self):
        rect_hits = pygame.sprite.spritecollide(self, self.game.items, False)
        if rect_hits:
            items = [self.get_mask_colliding_sprite([rect_hit]) for rect_hit in rect_hits]
            for item in items:
                if item and not item.is_picked_up:
                    type, item_info = item.picked_up()
                    if type == ItemType.COIN:
                        self.coins += item_info
                    elif type == ItemType.PICKUP_HEART:
                        self.heal(item_info)
                    elif type == ItemType.ITEM:
                        self.eq.add_item(item_info)
                    elif type == ItemType.PILL:
                        self.eq.use_pill(item_info)

    def get_center_position(self):
        return self.rect.centerx, self.rect.centery
    
    def set_rect_position(self, x_rect, y_rect):
        self.rect.x = x_rect
        self.rect.y = y_rect

    def get_hit(self, dmg:int):
        if self.immortality_time_left <= 0:
            self.health -= dmg * (1 - self.eq.stats["dmg_reduction"]) * self.eq.extra_stats["dmg_taken_multiplier"]
            self.immortality_time_left = self.get_immortality_time()
            self.check_is_dead()

    def check_is_dead(self):
        if self.health <= 0 and not GOD_MODE:
            self.is_alive = False
    
    def heal(self, amount:int):
        self.health = min(self.max_health, self.health + amount)

    def update_player_stats(self):
        self.max_health = BASE_HEALTH + self.eq.stats["health"]
        self.speed = (BASE_SPEED + self.eq.stats["speed"]) * self.game.settings.SCALE
    
    def get_shooting_cooldown(self):
        return int((BASE_SHOOTING_COOLDOWN - self.eq.stats["shooting_cooldown"]) * FPS)

    def get_immortality_time(self):
        return int((BASE_IMMORTALITY_AFTER_HIT + self.eq.stats["immortality"]) * FPS)

    def get_shot_speed(self):
        return BASE_SHOT_SPEED + self.eq.stats["shot_speed"]
    
    def get_luck(self):
        return BASE_LUCK + self.eq.stats["luck"]
    
    def spawn_pets(self, is_in_new_room:bool=True):
        pets_to_spawn = self.eq.extra_stats.get("friendly_ghost")
        if not is_in_new_room:
            FriendlyGhost(self.game, self.rect.centerx//self.game.settings.TILE_SIZE, 
                          self.rect.centery//self.game.settings.TILE_SIZE, pets_to_spawn%2!=1)
        else:
            for i in range(pets_to_spawn):
                FriendlyGhost(self.game, self.rect.centerx//self.game.settings.TILE_SIZE, 
                              self.rect.centery//self.game.settings.TILE_SIZE, i%2==1)
     
    def animate(self):
        self.reversed_body_frame = False
        if self.is_moving:
            self.time -= 1
        
        if self.time <= 0:
            self.time = self.next_frame_ticks_cd 
            self.x_legs_frame = (self.x_legs_frame + 1) % 10
        
        self.set_body_frame()
        if not self.is_moving:
            self.set_standing_frame()

        self.check_tear_animation()
        self.set_head_frame()
        self.next_frame()
        
    def check_tear_animation(self):
        self.head_tear_anime_time_left -= 1
        if self.head_tear_anime_time_left == self.head_tear_anime_cd - 1 or self.head_tear_anime_time_left == 1:
            self.x_head_frame = (self.x_head_frame + 1) % 2

    def set_standing_frame(self):
        self.body_frame = self.body_images[0]

    def next_frame(self):
        self.frame = pygame.Surface((self.PLAYER_SIZE, self.PLAYER_SIZE), pygame.SRCALPHA)
        if self.reversed_body_frame:
            self.body_frame = pygame.transform.flip(self.body_frame, True, False)

        self.frame.blit(self.body_frame, (0, self.PLAYER_SIZE*0.25))
        if self.reversed_head_frame:
            self.head_frame = pygame.transform.flip(self.head_frame, True, False)
        
        self.frame.blit(self.head_frame, ((self.PLAYER_SIZE - self.head_frame.get_width())//2, -3))
        self.image = self.frame
    
    def set_body_frame(self):
        if self.direction == Directions.LEFT or self.direction == Directions.RIGHT:
            self.x_legs_frame += 10
            if self.direction == Directions.LEFT: 
                self.reversed_body_frame = True
     
        self.body_frame = self.body_images[self.x_legs_frame]
        self.x_legs_frame %= 10
    
    def set_head_frame(self):
        x = self.x_head_frame
        self.reversed_head_frame = False
        if self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
            x += 2
            if self.facing == Directions.LEFT:
                self.reversed_head_frame = True
        elif self.facing == Directions.UP:
            x += 4
        
        self.head_frame = self.head_images[x]
        self.head_frame = pygame.transform.scale(self.head_frame, (self.PLAYER_SIZE*0.9, self.PLAYER_SIZE*0.9))
    
    def play_death_animation(self):
        center_x = self.rect.centerx
        cetner_y = self.rect.centery
        self.death_time_left -= 1
        if self.death_time_left <= 0:
            if self.death_index > self.last_death_index:
                self.end_of_death_animation = True
                return
            
            frame_name = "die" + str(self.death_index)
            self.image = self.game.image_loader.player_animation[frame_name]
            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()
            self.rect.centerx = center_x
            self.rect.centery = cetner_y

            self.death_time_left = self.death_frame_cd
            self.death_index += 1
    
    def update_rooms_cleared(self):
        self.rooms_cleared += 1
        self.rooms_cleared = min(self.rooms_cleared, ROOM_NUMBER - 2)
    
    def prepare_for_next_map(self):
        self.rooms_cleared = 0