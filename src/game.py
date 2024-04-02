import pygame
from map.map import *
from menu.button import *
from entities.player import *
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.intro_playing = True
        self.running = True
        self.playing = True
        self.intro_background = pygame.image.load("resources/menu/intro-background.png")
        self.intro_background = pygame.transform.smoothscale(self.intro_background, self.screen.get_size())
        self.font = pygame.font.Font(None, 50)
        
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
        
    def run(self):
        self.run_game()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

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


    def run_game(self):
        while self.running:
            self.events()
            if self.intro_playing:
                self.intro_screen()
            self.update()
            self.draw()

        self.running = False


    def game_over(self):
        pass

    def intro_screen(self):
        while self.intro_playing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    self.intro_playing = False

            self.screen.blit(self.intro_background, (0, 0))
            self.clock.tick(FPS)
            pygame.display.update()