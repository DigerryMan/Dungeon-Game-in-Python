import pygame
import sys
from map.map import *
from entities.player import *
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        self.playing = True
        
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 0, 0)
        self.map = Map(self, self.player)
        self.map.draw_initial_room()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        if len(self.enemies) == 0 or ADMIN:
            self.map.set_room_cleared()

    def render_next_room(self, direction:Directions):
        self._clear_sprites()
        self.map.draw_room(direction)

    def _clear_sprites(self):
        self.all_sprites.remove(self.blocks, self.doors, self.enemies, self.attacks)
        self.blocks.empty()
        self.doors.empty()
        self.attacks.empty()
        self.enemies.empty()
     

    def damage_player(self, enemy_dmg:int):
        self.player.get_hit(enemy_dmg)

    def draw(self):
        self.screen.fill(BLACK)
        #self.all_sprites.draw(self.screen)
        sprite_list = sorted(self.all_sprites, key=lambda sprite: sprite._layer)
        for sprite in sprite_list:
            self.screen.blit(sprite.image, sprite.rect)

        self.blocks.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

    def run_game(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def game_over(self):
        pass
