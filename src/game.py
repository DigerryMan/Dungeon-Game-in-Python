from entities.player.player_types import PlayerTypes
from entities.player.stat_bars import StatBars
import pygame
import os
from config import ADMIN, BLACK, FPS
from items.stat_items.items_list import ItemsList
from map.map import Map
from entities.player.player import Player
from menu import Menu
from utils.directions import Directions
from utils.image_loader import ImageLoader
from utils.settings import Settings

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

        self.character_type = PlayerTypes.ISAAC

        self.handle_resolution_change(window_size)
        self.sprite_groups = ["player_sprite", "entities", "all_sprites", "blocks", "shop_stands", "doors", 
                              "enemies", "not_voulnerable", "attacks", "chest", "items", "trap_door", "collidables"]
        self.not_clearable_groups = ["player_sprite"]
        self.init_empty_sprite_groups()

        self.prepare_game()

    def prepare_game(self):
        self.map = None
        self.player = None
        self.stat_bars = None

        self.difficulty = 1
        self.current_level = 0
        self.e_pressed = False
        self.space_pressed = False

    def handle_resolution_change(self, window_size):
        self.screen = pygame.display.set_mode(window_size)
        self.settings = Settings(window_size)
        self.image_loader = ImageLoader(self.settings)
        self.items_list = ItemsList(self)
        self.menu.update_images()

    def init_empty_sprite_groups(self):
        for group_name in self.sprite_groups:
            setattr(self, group_name, pygame.sprite.LayeredUpdates())

    def render_new_map(self, first_map = False):
        if first_map:
            self.prepare_game()
            
        self.current_level += 1
        self.init_empty_sprite_groups()
        if self.player is None:
            self.player = Player(self, 0, 0, self.character_type)

        else:
            self.player.prepare_for_next_map()
            self.all_sprites.add(self.player)
            self.player_sprite.add(self.player)
            self.entities.add(self.player)

        if self.stat_bars is None:
            self.stat_bars = StatBars(self, self.player)

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

    def draw(self):
        self.screen.fill(BLACK)

        self.map.get_current_room().draw(self.screen)
        self.map.draw_minimap(self.screen)
        self.stat_bars.update_and_draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def game_over(self):
        pass

    def render_next_room(self, direction:Directions):
        self.clear_sprites()
        self.map.render_next_room(direction)
        self.get_new_sprites(self.map.get_current_room())

    def clear_sprites(self):
        for group_name in self.sprite_groups:
            if group_name not in self.not_clearable_groups:
                getattr(self, group_name).empty()
     
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