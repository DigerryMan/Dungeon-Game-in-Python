import pygame
from config import *
from entities.mobs.friendly_ghost import FriendlyGhost
from entities.player.equipment import Equipment
from items.item_types import ItemType
from ..bullet import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        #MAIN
        self.game = game
        self.max_health = BASE_HEALTH
        self.health = BASE_HEALTH
        self.__speed = BASE_SPEED
        self.coins = 0

        #SIZE
        self.width = game.settings.PLAYER_SIZE
        self.height = game.settings.PLAYER_SIZE

        #SKIN
        self.image = pygame.Surface([self.width, self.height])

        self.x_legs_frame = 0
        self.x_head_frame = 0
        self.next_head_frame = 0
        self.y_frame = 0
        self.reversed_frame = False
        
        #ANIMATION SPEED
        self.next_frame_ticks_cd = 3
        self.time = 0
        self.next_head_frame_ticks_cd = 20
        self.head_frame_time = 0

        self.PLAYER_SIZE = game.settings.PLAYER_SIZE
        self.img = game.image_loader.get_image("player")
        self.frame = self.img.subsurface(pygame.Rect(self.x_legs_frame, 0, 32, 32))
        self.frame = pygame.transform.scale(self.frame, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.head_frame = None
        self.body_frame = None
        self.is_moving = False

        
        #HITBOX / POSITION
        self.rect = self.image.get_rect()
        self.rect.x = x * self.width
        self.rect.y = y * self.height
        
        #EQ
        self.eq = Equipment(self)
        self.eq_opened = False
        
        #REST
        self._layer = self.rect.bottom
        self.__immortality_time_left = 0
        self.__shot_time_left = 0
        self.facing = Directions.DOWN
        self.direction = Directions.DOWN
        self.last_horizontall_facing = Directions.RIGHT
        self.x_change = 0
        self.y_change = 0
        
        self.groups = self.game.all_sprites, self.game.player_sprite, self.game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animate()
        self.mask = pygame.mask.from_surface(self.image)

        removed_hitbox_from_sides = pygame.Surface((self.mask.get_size()[1] * 0.2, self.mask.get_size()[1]))
        removed_hitbox_from_top = pygame.Surface((self.mask.get_size()[0], self.mask.get_size()[0] * 0.25))
        cut_mask_sides = pygame.mask.from_surface(removed_hitbox_from_sides)
        cut_mask_top = pygame.mask.from_surface(removed_hitbox_from_top)

        self.mask.erase(cut_mask_sides, (0, 0))
        self.mask.erase(cut_mask_sides, (self.mask.get_size()[0] - cut_mask_sides.get_size()[0], 0))
        self.mask.erase(cut_mask_top, (0, 0))
    
    def update(self):
        self._user_input()
        self._correct_diagonal_movement()

        self.rect.x += self.x_change
        self._collide_blocks('x')
        self.rect.y += self.y_change
        self._collide_blocks('y')

        self._check_items_pick_up()
        self._layer = self.rect.bottom
        self.animate()

        self.__immortality_time_left -= 1
        self.x_change = 0
        self.y_change = 0

    def _user_input(self):
        keys = pygame.key.get_pressed()
        x_y_vel = [0,0]
        self.is_moving = False
        self._move(keys, x_y_vel)
        self._shoot(keys, x_y_vel)

    def _move(self, keys, x_y_vel):
        if keys[pygame.K_a]:
            self.x_change -= self.__speed
            self.facing = Directions.LEFT
            self.last_horizontall_facing = Directions.LEFT
            x_y_vel[0] -= 1
            self.is_moving = True
        
        if keys[pygame.K_d]:
            self.x_change += self.__speed
            self.facing = Directions.RIGHT
            self.last_horizontall_facing = Directions.RIGHT
            x_y_vel[0] += 1
            self.is_moving = True

        if keys[pygame.K_w]: 
            self.y_change -= self.__speed
            self.facing = Directions.UP
            x_y_vel[1] -= 1
            self.is_moving = True

        if keys[pygame.K_s]:
            self.y_change += self.__speed
            self.facing = Directions.DOWN
            x_y_vel[1] += 1
            self.is_moving = True

    def _shoot(self, keys, x_y_vel):
        self.__shot_time_left -= 1
        if self.__shot_time_left <= 0:
            shot = False
            if keys[pygame.K_LEFT]:
                self.direction = Directions.LEFT
                shot = True

            if keys[pygame.K_RIGHT]:
                self.direction = Directions.RIGHT
                shot = True

            if keys[pygame.K_UP]:
                self.direction = Directions.UP
                shot = True

            if keys[pygame.K_DOWN]:
                self.direction = Directions.DOWN
                shot = True
            
            if shot:
                self.__shot_time_left = self.get_shooting_cooldown()
                additional_v = 0
                
                if PLAYER_SHOOT_DIAGONAL:
                    _, other_axis_index = self.direction.rotate_clockwise().get_axis_tuple()     
                    if x_y_vel[other_axis_index]:
                        additional_v = int(self.get_shot_speed() * x_y_vel[other_axis_index] * DIAGONAL_MULTIPLIER) 

                x, y = self.calculate_bullet_position()

                Bullet(self.game, x, y, self.direction, self.get_shot_speed(), True,
                        (BASE_DMG+self.eq.stats["dmg"])*self.eq.extra_stats["dmg_multiplier"], BASE_BULLET_FLY_TIME+self.eq.stats["bullet_fly_time"],
                       additional_speed=additional_v)

    def calculate_bullet_position(self):
        x, y = self.rect.centerx, self.rect.centery
        if self.direction == Directions.LEFT:
            x -= self.PLAYER_SIZE//2
        elif self.direction == Directions.RIGHT:
            x += self.PLAYER_SIZE//2
        elif self.direction == Directions.UP:
            y -= self.PLAYER_SIZE//2
        elif self.direction == Directions.DOWN:
            y += self.PLAYER_SIZE//2
        return x, y

    def _correct_diagonal_movement(self):
        if(self.x_change and self.y_change):
            self.x_change //= 1.41
            self.y_change //= 1.41
            if self.x_change < 0:
                self.x_change += 1
            if self.y_change < 0:
                self.y_change += 1
                
    def _collide_blocks(self, direction:str):
        hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if hits:
            mask_hits = pygame.sprite.spritecollide(self, self.game.collidables, False, pygame.sprite.collide_mask)
            if mask_hits:  
                if direction == 'x':
                    self.rect.x -= self.x_change

                if direction == 'y':
                    self.rect.y -= self.y_change

    def _check_items_pick_up(self):
        hits = pygame.sprite.spritecollide(self, self.game.items, False)
        if hits:
            mask_hits = pygame.sprite.spritecollide(self, self.game.items, False, pygame.sprite.collide_mask)
            for item in mask_hits:
                if not item.is_picked_up:
                    type, item_info = item.picked_up()
                    
                    if type == ItemType.COIN:
                        self.coins += item_info

                    elif type == ItemType.HEALTH_POTION:
                        self.heal(item_info)

                    elif type == ItemType.ITEM:
                        self.eq.add_item(item_info)

    def set_rect_position(self, x_rect, y_rect):
        self.rect.x = x_rect
        self.rect.y = y_rect

    def get_hit(self, dmg:int):
        if self.__immortality_time_left <= 0:
            self.health -= dmg * (1 - self.eq.stats["dmg_reduction"]) * self.eq.extra_stats["dmg_taken_multiplier"]
            self.__immortality_time_left = self.get_immortality_time()
            print(self.health)
            self._check_is_dead()

    def _check_is_dead(self):
        if self.health <= 0 and not GOD_MODE:
            self.game.game_over()
    
    def get_center_position(self):
        return self.rect.centerx, self.rect.centery
    
    def heal(self, amount:int):
        self.health = min(self.max_health, self.health + amount)

    def update_player_stats(self):
        self.max_health = BASE_HEALTH + self.eq.stats["health"]
        self.__speed = BASE_SPEED + self.eq.stats["speed"]
    
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
        frame_change = False
        self.head_frame_time -= 1
        if self.is_moving:
            self.time -= 1
        else:
            self.set_standing_frame()

        if self.head_frame_time <= 0:
            self.head_frame_time = self.next_head_frame_ticks_cd
            self.next_head_frame = (self.next_head_frame + 1) % 2
            frame_change = True
            self.set_head_frame()

        
        if self.time <= 0:
            self.time = self.next_frame_ticks_cd 
            self.x_legs_frame = (self.x_legs_frame + 1) % 10
            frame_change = True
            self.set_body_frame()

        if frame_change:
            self.next_frame()

    def set_standing_frame(self):
        self.body_frame = self.img.subsurface(pygame.Rect(0 * 32, 1 * 32, 32, 32))
        self.body_frame = pygame.transform.scale(self.body_frame, (self.PLAYER_SIZE, self.PLAYER_SIZE))

    def next_frame(self):
        self.frame = pygame.Surface((self.PLAYER_SIZE, self.PLAYER_SIZE), pygame.SRCALPHA)

        self.frame.blit(self.body_frame, (0, self.PLAYER_SIZE*0.25))
        self.frame.blit(self.head_frame, ((self.PLAYER_SIZE - self.head_frame.get_width())//2, -3))
        
        if self.reversed_frame:
            self.frame = pygame.transform.flip(self.frame, True, False)

        self.remove_transparency_from_frame()
    
    def set_body_frame(self):
        self.reversed_frame = False
        if self.facing == Directions.LEFT:
            self.y_frame = 2
            self.reversed_frame = True
        elif self.facing == Directions.RIGHT:
            self.y_frame = 2
        elif self.facing == Directions.UP or self.facing == Directions.DOWN:
            self.y_frame = 1
        
        self.body_frame = self.img.subsurface(pygame.Rect(self.x_legs_frame * 32, self.y_frame * 32, 32, 32))
        self.body_frame = pygame.transform.scale(self.body_frame, (self.PLAYER_SIZE, self.PLAYER_SIZE))
    
    def set_head_frame(self):
        x = self.next_head_frame
        if self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
            x += 2
        if self.facing == Directions.UP:
            x += 4
        
        self.head_frame = self.img.subsurface(pygame.Rect(x * 32, 0, 32, 32))
        self.head_frame = pygame.transform.scale(self.head_frame, (self.PLAYER_SIZE*0.9, self.PLAYER_SIZE*0.9))

    def remove_transparency_from_frame(self):
        #bounding_rect = self.frame.get_bounding_rect() 
        #self.image = self.frame.subsurface(bounding_rect)
        #self.rect.width, self.rect.height = self.image.get_rect().width, self.image.get_rect().height 
        self.image = self.frame
        #self.mask = pygame.mask.from_surface(self.image)        