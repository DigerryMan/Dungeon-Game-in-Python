import pygame
from map.map import *
from menu.button import *
from entities.player.player import *
from config import *
from utils.image_loader import ImageLoader
from utils.settings import *

class Game:
    def __init__(self):
        pygame.init()

        #nie ruszac
        #self.screen = pygame.display.set_mode((0, 0))
        #window_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        #window_size = (1920, 1080)
        window_size = (1280, 720)
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        

        self.settings = Settings(window_size)

        self.clock = pygame.time.Clock()
        self.intro_playing = True
        self.menu_playing = False
        self.running = True
        self.paused = False

        self.e_pressed = False

        self.image_loader = ImageLoader()
          
        self.const_intro_background = pygame.image.load("resources/menu/introbackground.png")
        self.intro_background = pygame.transform.smoothscale(self.const_intro_background, self.screen.get_size())
        self.const_menu_card = pygame.image.load("resources/menu/menucard.png")
        self.menu_card = pygame.transform.smoothscale(self.const_menu_card, self.screen.get_size())
        self.const_settings_card = pygame.image.load("resources/menu/settingscard.png")
        self.settings_card = pygame.transform.smoothscale(self.const_settings_card, self.screen.get_size())
        self.const_menu_background = pygame.image.load("resources/menu/menuoverlay.png")
        self.menu_background = pygame.transform.smoothscale(self.const_menu_background, self.screen.get_size())
        self.const_pause_card = pygame.image.load("resources/menu/pausecard2.png")
        self.pause_card = pygame.transform.smoothscale(self.const_pause_card, (self.const_pause_card.get_height() * self.settings.SCALE, self.const_pause_card.get_width() * self.settings.SCALE))
        self.const_arrow = pygame.image.load("resources/menu/arrow2.png")
        self.arrow = pygame.transform.smoothscale(self.const_arrow, (self.const_arrow.get_width() * 0.7 * self.settings.SCALE, self.const_arrow.get_height() * 0.7 * self.settings.SCALE))
        self.const_main_title = pygame.image.load("resources/menu/maintitle.png")
        self.main_title = pygame.transform.scale(self.const_main_title, (self.const_main_title.get_width() * 2.8 * self.settings.SCALE, self.const_main_title.get_height() * 2.8 * self.settings.SCALE))
        self.font = pygame.font.SysFont("arialblack", 30)
        
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.not_voulnerable = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.chest = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()

        #for collision detection
        self.collidables = pygame.sprite.LayeredUpdates()

        self.map = None
        self.player = None


    def handle_resolution_change(self, window_size):
        self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        self.settings = Settings(window_size)

        self.intro_background = pygame.transform.smoothscale(self.const_intro_background, self.screen.get_size())
        self.menu_card = pygame.transform.smoothscale(self.const_menu_card, self.screen.get_size())
        self.settings_card = pygame.transform.smoothscale(self.const_settings_card, self.screen.get_size())
        self.menu_background = pygame.transform.smoothscale(self.const_menu_background, self.screen.get_size())
        self.pause_card = pygame.transform.smoothscale(self.const_pause_card, (self.const_pause_card.get_height() * self.settings.SCALE, self.const_pause_card.get_width() * self.settings.SCALE))
        self.arrow = pygame.transform.smoothscale(self.const_arrow, (self.const_arrow.get_width() * 0.7 * self.settings.SCALE, self.const_arrow.get_height() * 0.7 * self.settings.SCALE))
        self.main_title = pygame.transform.scale(self.const_main_title, (self.const_main_title.get_width() * 2.8 * self.settings.SCALE, self.const_main_title.get_height() * 2.8 * self.settings.SCALE))

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

        pygame.quit()

    def render_new_map(self):
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.not_voulnerable = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.chest = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()

        #for collision detection
        self.collidables = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 0, 0)
        self.map = Map(self, self.player)
        self.map.render_initial_room()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

                if event.key == pygame.K_e:
                    self.e_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    self.e_pressed = False


    def update(self):
        self.all_sprites.update()
        self.blocks.update()
        self.items.update()
        if len(self.enemies) == 0 or ADMIN:
            self.collidables.remove(self.doors)
            self.map.set_room_cleared()


    def render_next_room(self, direction:Directions):
        self._clear_sprites()
        self.map.render_next_room(direction)
        self._get_new_sprites(self.map.get_current_room())


    def _clear_sprites(self):
        self.all_sprites.remove(self.blocks, self.doors, self.enemies, self.attacks)
        self.blocks.empty()
        self.doors.empty()
        self.attacks.empty()
        self.enemies.empty()
        self.collidables.empty()
        self.not_voulnerable.empty()
        self.chest.empty()
        self.items.empty()
     

    def _get_new_sprites(self, room):
        objects = room.get_objects()
        self.blocks.add(objects["blocks"])
        self.doors.add(objects["doors"])
        if objects["chest"]:
            self.chest.add(objects["chest"])
            self.collidables.add(objects["chest"])
        self.items.add(objects["items"])
        self.enemies.add(objects["enemies"])
        self.collidables.add(objects["blocks"])
        self.collidables.add(objects["walls"])
        self.all_sprites.add(self.blocks, self.doors, self.enemies, self.attacks)


    def damage_player(self, enemy_dmg:int):
        self.player.get_hit(enemy_dmg)


    def get_player_rect(self):
        return self.player.rect


    def draw(self):
        self.screen.fill(BLACK)

        self.collidables.draw(self.screen)
        self.items.draw(self.screen)
        
        sprite_list = sorted(self.all_sprites, key=lambda sprite: sprite._layer)
        for sprite in sprite_list:
            self.screen.blit(sprite.image, sprite.rect)

        
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
        arrow_positions = [(self.settings.WIN_WIDTH//2.5, self.settings.WIN_HEIGHT//3.15), 
                           (self.settings.WIN_WIDTH//2.44, self.settings.WIN_HEIGHT//2.2), 
                           (self.settings.WIN_WIDTH//2.43, self.settings.WIN_HEIGHT//1.67)]
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
                            arrow_positions = [(self.settings.WIN_WIDTH//2.5, self.settings.WIN_HEIGHT//3.15), 
                                            (self.settings.WIN_WIDTH//2.44, self.settings.WIN_HEIGHT//2.2), 
                                            (self.settings.WIN_WIDTH//2.43, self.settings.WIN_HEIGHT//1.67)]

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

        arrow_positions = [(self.settings.WIN_WIDTH//2.55, self.settings.WIN_HEIGHT//3.1), 
                    (self.settings.WIN_WIDTH//2.5, self.settings.WIN_HEIGHT//2.35), 
                    (self.settings.WIN_WIDTH//2.48, self.settings.WIN_HEIGHT//1.91)]
        current_arrow = 0

        while settings_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    settings_playing = False
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        current_arrow = current_arrow + 1 if current_arrow < 2 else 0

                    if event.key == pygame.K_UP:
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 2

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.handle_resolution_change((1920, 1080))
                            arrow_positions = [(self.settings.WIN_WIDTH//2.55, self.settings.WIN_HEIGHT//3.1), 
                                            (self.settings.WIN_WIDTH//2.5, self.settings.WIN_HEIGHT//2.35), 
                                            (self.settings.WIN_WIDTH//2.48, self.settings.WIN_HEIGHT//1.91)]
                        elif current_arrow == 1:
                            self.handle_resolution_change((1600, 900))
                            arrow_positions = [(self.settings.WIN_WIDTH//2.55, self.settings.WIN_HEIGHT//3.1), 
                                            (self.settings.WIN_WIDTH//2.5, self.settings.WIN_HEIGHT//2.35), 
                                            (self.settings.WIN_WIDTH//2.48, self.settings.WIN_HEIGHT//1.91)]
                        elif current_arrow == 2:
                            self.handle_resolution_change((1280, 720))
                            arrow_positions = [(self.settings.WIN_WIDTH//2.55, self.settings.WIN_HEIGHT//3.1), 
                                            (self.settings.WIN_WIDTH//2.5, self.settings.WIN_HEIGHT//2.35), 
                                            (self.settings.WIN_WIDTH//2.48, self.settings.WIN_HEIGHT//1.91)]

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