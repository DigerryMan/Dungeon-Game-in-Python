import pygame
import os
from items.stat_items.items_list import ItemsList
from map.map import *
from entities.player.player import *
from config import *
from utils.image_loader import ImageLoader
from utils.settings import *

class Game:
    def __init__(self):
        pygame.init()

        window_size = (1920, 1080)
        #window_size = (1280, 720)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        

        self.settings = Settings(window_size)
        self.image_loader = ImageLoader(self.settings)
        self.items_list = ItemsList(self)

        self.clock = pygame.time.Clock()
        self.intro_playing = True
        self.menu_playing = False
        self.running = True
        self.paused = False

        self.e_pressed = False
        self.space_pressed = False

        self.handle_resolution_change(window_size)  
                
        self.font = pygame.font.SysFont("arialblack", 30)
        
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.entities = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.not_voulnerable = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.chest = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()
        self.trap_door = pygame.sprite.LayeredUpdates()
        self.collidables = pygame.sprite.LayeredUpdates()

        self.map = None
        self.current_level = 1
        self.player = None


    def handle_resolution_change(self, window_size):
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        self.settings = Settings(window_size)
        self.image_loader = ImageLoader(self.settings)
        self.items_list = ItemsList(self)

        self.intro_background = self.image_loader.get_image("introbackground")
        self.menu_card = self.image_loader.get_image("menucard")
        self.settings_card = self.image_loader.get_image("settingscard")
        self.menu_background = self.image_loader.get_image("menuoverlay")
        self.pause_card = self.image_loader.get_image("pausecard2")
        self.arrow = self.image_loader.get_image("arrow2")
        self.main_title = self.image_loader.get_image("maintitle")


    def run(self):
        self.intro_screen()
        while self.running:
            self.events()
            self.main_menu()

            if not self.paused and self.running:
                self.update()
                self.draw()

            if self.paused:
                self.display_pause()
            
            if self.player is not None and self.player.eq_opened:
                self.display_eq()

        pygame.quit()


    def render_new_map(self):
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.entities = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
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
        self._clear_sprites()
        self.map.render_next_room(direction)
        self._get_new_sprites(self.map.get_current_room())


    def _clear_sprites(self):
        self.all_sprites.empty()
        self.blocks.empty()
        self.doors.empty()
        self.attacks.empty()
        self.enemies.empty()
        self.collidables.empty()
        self.not_voulnerable.empty()
        self.chest.empty()
        self.items.empty()
        self.entities.empty()
        self.trap_door.empty()
     

    def _get_new_sprites(self, room):
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


    def intro_screen(self):
        while self.intro_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.intro_playing = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN)):
                    self.intro_playing = False
                    self.menu_playing = True

            self.screen.blit(self.intro_background, (0, 0))
            self.clock.tick(FPS)
            pygame.display.update()


    def main_menu(self):
        arrow_positions = [(self.settings.WIN_WIDTH//2.35, self.settings.WIN_HEIGHT//3.13), 
                           (self.settings.WIN_WIDTH//2.44, self.settings.WIN_HEIGHT//2.15), 
                           (self.settings.WIN_WIDTH//2.27, self.settings.WIN_HEIGHT//1.67)]
        current_arrow = 0

        while self.menu_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_playing = False
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        current_arrow = current_arrow + 1 if current_arrow < 2 else 0

                    if event.key == pygame.K_UP:
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 2

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.menu_playing = False
                            self.render_new_map()
                            self.paused = False

                        elif current_arrow == 1:
                            self.menu_playing = False
                            self.settings_playing = True
                            self.display_settings()
                            arrow_positions = [(self.settings.WIN_WIDTH//2.35, self.settings.WIN_HEIGHT//3.13), 
                                            (self.settings.WIN_WIDTH//2.44, self.settings.WIN_HEIGHT//2.15), 
                                            (self.settings.WIN_WIDTH//2.27, self.settings.WIN_HEIGHT//1.67)]
                            
                            if not self.menu_playing:
                                return

                        elif current_arrow == 2:
                            self.menu_playing = False
                            self.running = False

            self.screen.blit(self.menu_card, (0, 0))
            self.screen.blit(self.menu_background, (0, 0))
            self.screen.blit(self.main_title, (self.settings.WIN_WIDTH//8, 0))

            self.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.clock.tick(FPS)
            pygame.display.update()


    def display_settings(self):
        settings_playing = True

        arrow_positions = [(self.settings.WIN_WIDTH//2.52, self.settings.WIN_HEIGHT//2.78), 
                    (self.settings.WIN_WIDTH//2.48, self.settings.WIN_HEIGHT//2.13), 
                    (self.settings.WIN_WIDTH//2.43, self.settings.WIN_HEIGHT//1.72)]
        current_arrow = 0

        while settings_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    settings_playing = False
                    self.menu_playing = False
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        current_arrow = current_arrow + 1 if current_arrow < 2 else 0

                    if event.key == pygame.K_UP:
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 2

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.handle_resolution_change((1920, 1080))
                            arrow_positions = [(self.settings.WIN_WIDTH//2.52, self.settings.WIN_HEIGHT//2.78), 
                                        (self.settings.WIN_WIDTH//2.48, self.settings.WIN_HEIGHT//2.13), 
                                        (self.settings.WIN_WIDTH//2.43, self.settings.WIN_HEIGHT//1.72)]
                        elif current_arrow == 1:
                            self.handle_resolution_change((1600, 900))
                            arrow_positions = [(self.settings.WIN_WIDTH//2.52, self.settings.WIN_HEIGHT//2.78), 
                                        (self.settings.WIN_WIDTH//2.48, self.settings.WIN_HEIGHT//2.13), 
                                        (self.settings.WIN_WIDTH//2.43, self.settings.WIN_HEIGHT//1.72)]
                        elif current_arrow == 2:
                            self.handle_resolution_change((1280, 720))
                            arrow_positions = [(self.settings.WIN_WIDTH//2.52, self.settings.WIN_HEIGHT//2.78), 
                                        (self.settings.WIN_WIDTH//2.48, self.settings.WIN_HEIGHT//2.13), 
                                        (self.settings.WIN_WIDTH//2.43, self.settings.WIN_HEIGHT//1.72)]

                    if event.key == pygame.K_ESCAPE:
                        settings_playing = False
                        self.menu_playing = True


            self.screen.blit(self.settings_card, (0, 0))
            self.screen.blit(self.menu_background, (0, 0))
            self.screen.blit(self.main_title, (self.settings.WIN_WIDTH//8, 0))

            self.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.clock.tick(FPS)
            pygame.display.update()


    def display_pause(self):
        arrow_positions = [(self.settings.WIN_WIDTH//2.82, self.settings.WIN_HEIGHT//1.55),
                           (self.settings.WIN_WIDTH//2.62, self.settings.WIN_HEIGHT//1.38)]
        current_arrow = 0

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.paused = False
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False
                    
                    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        current_arrow = current_arrow + 1 if current_arrow == 0 else 0

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.paused = False
                        elif current_arrow == 1:
                            self.paused = False
                            self.menu_playing = True

            self.screen.blit(self.pause_card, (self.settings.WIN_WIDTH//4, self.settings.WIN_HEIGHT//20))
            self.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.clock.tick(FPS)
            pygame.display.update()


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