import pygame
from config import *
from .bullet import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name="Player1"):
        self.__health = 3
        self.__movement_speed = 100
        self.__name = name
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.speed = 10
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.facing = Directions.DOWN

        self.x_change = 0
        self.y_change = 0

        self.game = game
        self.groups = self.game.all_sprites, self.game.player_sprite

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self._layer = self.rect.bottom
        self.__last_hit = pygame.time.get_ticks()
        self.__immortality_after_hit = 1000
        self.__shooting_cooldown = 500
        self.__last_shot = pygame.time.get_ticks()


        pygame.sprite.Sprite.__init__(self, self.groups)
    
    def _user_input(self):
        keys = pygame.key.get_pressed()
        self._move(keys)
        self._shoot(keys)

    def _move(self, keys):
        if keys[pygame.K_a]:
            self.x_change -= self.speed
            self.facing = Directions.LEFT
        
        if keys[pygame.K_d]:
            self.x_change += self.speed
            self.facing = Directions.RIGHT


        if keys[pygame.K_w]: 
            self.y_change -= self.speed
            self.facing = Directions.UP


        if keys[pygame.K_s]:
            self.y_change += self.speed
            self.facing = Directions.DOWN

    def _shoot(self, keys):
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.__last_shot > self.__shooting_cooldown:
                self.__last_shot = now
                Bullet(self.game, self.rect.centerx, self.rect.centery, self.facing)
            pass

    def update(self):
        self._user_input()
        
        self._correct_diagonal_movement()

        self.rect.x += self.x_change
        self._collide_blocks('x')
        self.rect.y += self.y_change
        self._collide_blocks('y')

        self._layer = self.rect.bottom

        self.x_change = 0
        self.y_change = 0
    


    def _correct_diagonal_movement(self):
        if(self.x_change and self.y_change):
            self.x_change //= 1.41
            self.y_change //= 1.41
            if self.x_change < 0:
                self.x_change += 1
            if self.y_change < 0:
                self.y_change += 1

    def _collide_blocks(self, direction:str):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

            if direction == 'y':
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def set_rect_position(self, x_rect, y_rect):
        self.rect.x = x_rect
        self.rect.y = y_rect

    def get_hit(self, dmg:int):
        now = pygame.time.get_ticks()
        if now - self.__last_hit > self.__immortality_after_hit:
            self.__health -= dmg
            self.__last_hit = now
            if self.__health <= 0:
                self.game.game_over()
                print("KONIEC GRY!")
            print(self.__health)

    