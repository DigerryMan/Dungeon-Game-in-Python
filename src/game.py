import pygame
import os
from items.stat_items.items_list import ItemsList
from map.map import *
from entities.player.player import *
from config import *
from menu import Menu
from utils.image_loader import ImageLoader
from utils.settings import *

class Game:
    def __init__(self):
        pygame.init()

        #window_size = (1920, 1080)
        window_size = (1280, 720)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode(window_size)
        

        self.settings = Settings(window_size)
        self.image_loader = ImageLoader(self.settings)
        self.items_list = ItemsList(self)
        self.menu = Menu(self)

        self.clock = pygame.time.Clock()
        self.intro_playing = True
        self.menu_playing = False
        self.running = True
        self.paused = False

        self.e_pressed = False
        self.space_pressed = False

        self.handle_resolution_change(window_size)
        
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.entities = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.shop_stands = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.not_voulnerable = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.chest = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()
        self.trap_door = pygame.sprite.LayeredUpdates()
        self.collidables = pygame.sprite.LayeredUpdates()

        self.difficulty = 1
        self.map = None
        self.current_level = 1
        self.player = None


    def handle_resolution_change(self, window_size):
        self.screen = pygame.display.set_mode(window_size)
        self.settings = Settings(window_size)
        self.image_loader = ImageLoader(self.settings)
        self.items_list = ItemsList(self)
        self.menu.update_images()


    def render_new_map(self):
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.entities = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.shop_stands = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.not_voulnerable = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.chest = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()
        self.trap_door = pygame.sprite.LayeredUpdates()
        self.collidables = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 0, 0)
        self.map = Map(self, self.player, self.current_level)
        self.map.render_initial_room()


    def run(self):
        self.menu.intro_screen()

        while self.running:
            self.events()

            if self.menu_playing:
                self.menu.main_menu()

            if not self.paused and self.running:
                self.update()
                self.draw()

            if self.paused:
                self.menu.display_pause()
            
            if self.player is not None and self.player.eq_opened:
                self.display_eq()

        pygame.quit()


    def events(self):
        self.e_pressed = False
        self.space_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

                if event.key == pygame.K_e:
                    self.e_pressed = True

                if event.key == pygame.K_SPACE:
                    self.space_pressed = True

                if event.key == pygame.K_TAB:
                    self.player.eq_opened = not self.player.eq_opened


    def update(self):
        self.all_sprites.update()
        if not self.map.get_current_room().is_cleared and len(self.enemies) == 0 or ADMIN:
            self.collidables.remove(self.doors)
            self.map.set_room_cleared()


    def render_next_room(self, direction:Directions):
        self.clear_sprites()
        self.map.render_next_room(direction)
        self.get_new_sprites(self.map.get_current_room())


    def clear_sprites(self):
        self.all_sprites.empty()
        self.blocks.empty()
        self.shop_stands.empty()
        self.doors.empty()
        self.attacks.empty()
        self.enemies.empty()
        self.collidables.empty()
        self.not_voulnerable.empty()
        self.chest.empty()
        self.items.empty()
        self.entities.empty()
        self.trap_door.empty()
     

    def get_new_sprites(self, room):
        self.all_sprites.add(self.player_sprite)
        objects = room.get_objects()
        self.blocks.add(objects["blocks"])
        self.doors.add(objects["doors"])
        if objects["chest"]:
            self.chest.add(objects["chest"])
            self.collidables.add(objects["chest"])
            self.all_sprites.add(self.chest)

        if objects["trap_door"]:
            self.trap_door.add(objects["trap_door"])
            self.all_sprites.add(objects["trap_door"])

        if objects["shop_stands"]:
            self.shop_stands.add(objects["shop_stands"])
            self.all_sprites.add(self.shop_stands)

        self.items.add(objects["items"])
        self.enemies.add(objects["enemies"])
        self.collidables.add(objects["blocks"])
        self.collidables.add(objects["walls"])
        self.all_sprites.add(self.collidables, self.doors, self.enemies, self.attacks, self.items)
        self.entities.add(self.enemies, self.player_sprite)


    def damage_player(self, enemy_dmg:int):
        self.player.get_hit(enemy_dmg)


    def get_player_rect(self):
        return self.player.rect


    def draw(self):
        self.screen.fill(BLACK)

        self.map.get_current_room().draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()


    def game_over(self):
        pass


    def display_eq(self):
        self.player.eq.user_eq_input(None) #show big_item first time
        
        while(self.player.eq_opened):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.player.eq_opened = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE:
                        self.player.eq_opened = False

                    self.player.eq.user_eq_input(event.key)

            self.player.eq.draw(self.screen)
            self.clock.tick(FPS)
            pygame.display.update()