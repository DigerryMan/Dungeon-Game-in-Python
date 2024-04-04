import pygame
from map.map import *
from menu.button import *
from entities.player import *
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), not ADMIN and pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.intro_playing = True
        self.menu_playing = False
        self.running = True
        self.paused = False

        self.intro_background = pygame.image.load("resources/menu/introbackground.png")
        self.intro_background = pygame.transform.smoothscale(self.intro_background, self.screen.get_size())
        self.menu_background = pygame.image.load("resources/menu/menuoverlay.png")
        self.menu_background = pygame.transform.smoothscale(self.menu_background, self.screen.get_size())
        self.main_title = pygame.image.load("resources/menu/maintitle.png")
        title_width = WIN_WIDTH // 2
        title_height = self.main_title.get_height() * title_width // self.main_title.get_width()
        self.main_title = pygame.transform.scale(self.main_title, (title_width, title_height))
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

        self.player = None
        self.map = None

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

    def update(self):
        self.all_sprites.update()
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

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    self.intro_playing = False
                    self.menu_playing = True

            self.screen.blit(self.intro_background, (0, 0))
            self.clock.tick(FPS)
            pygame.display.update()

    def main_menu(self):
        play_button = Button(WIN_WIDTH/2 - 100, WIN_HEIGHT/2, 200, 50, "Play", WHITE, self.font, 40)
        quit_button = Button(WIN_WIDTH/2 - 100, WIN_HEIGHT/2 + 100, 200, 50, "Quit", WHITE, self.font, 40)

        while self.menu_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_playing = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_pressed(pygame.mouse.get_pos()):
                        self.menu_playing = False
                        self.render_new_map()
                        self.paused = False

                    if quit_button.is_pressed(pygame.mouse.get_pos()):
                        self.menu_playing = False
                        self.running = False
                

            self.screen.fill(DARK_GREY)
            self.screen.blit(self.menu_background, (0, 0))
            
            title_rect = self.main_title.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/4))
            self.screen.blit(self.main_title, title_rect)
            
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def display_pause(self):
        resume_button = Button(WIN_WIDTH/2 - 100, WIN_HEIGHT/2, 200, 50, "Resume", WHITE, self.font, 40)
        menu_button = Button(WIN_WIDTH/2 - 100, WIN_HEIGHT/2 + 100, 200, 50, "Menu", WHITE, self.font, 40)

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.paused = False
                    self.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.paused = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.is_pressed(pygame.mouse.get_pos()):
                        self.paused = False

                    if menu_button.is_pressed(pygame.mouse.get_pos()):
                        self.paused = False
                        self.menu_playing = True

            self.screen.blit(resume_button.image, resume_button.rect)
            self.screen.blit(menu_button.image, menu_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()