import pygame
from config import FPS

class BossIntroScreen():
    def __init__(self, menu):
        self.menu = menu
        self.game = menu.game
        self.start_time = None

    def display(self, boss):
        should_display = True
        self.start_time = pygame.time.get_ticks()

        boss_spot = self.game.image_loader.boss_intro["bossspot"]
        boss_spot_position = (self.game.settings.WIN_WIDTH//2.3, self.game.settings.WIN_HEIGHT//1.7)

        player_spot = self.game.image_loader.boss_intro["spot1"]
        player_spot_position = (self.game.settings.WIN_WIDTH//20, self.game.settings.WIN_HEIGHT//1.4)

        boss_image = boss.animation.intro_image
        boss_image_position = (boss_spot_position[0] + boss_spot.get_width()//2 - boss_image.get_width()//2,
                               boss_spot_position[1] + boss_spot.get_height()//2 - boss_image.get_height())
        
        player_image = self.game.player.animation.intro_image
        player_image_position = (player_spot_position[0] + player_spot.get_width()//2 - player_image.get_width()//2,
                                 player_spot_position[1] + player_spot.get_height()//2 - player_image.get_height()//1.5)

        vs = self.game.image_loader.boss_intro["vs"]

        while should_display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.paused = False
                    self.game.running = False
                    should_display = False
                
            if (pygame.time.get_ticks() - self.start_time) > 5000:
                should_display = False

            self.game.screen.fill((0, 0, 0))
            
            self.game.screen.blit(player_spot, player_spot_position)
            self.game.screen.blit(boss_spot, boss_spot_position)
            self.game.screen.blit(boss_image, boss_image_position)
            self.game.screen.blit(player_image, player_image_position)
            self.display_names(self.game.player.animation.intro_name, vs, boss.animation.intro_name)
            self.game.clock.tick(FPS)
            pygame.display.update()

    def display_names(self, player_name, vs, boss_name):
        vs_position = (self.game.settings.WIN_WIDTH//5, self.game.settings.WIN_HEIGHT//5)
        player_name_position = (vs_position[0] + vs.get_width()//2 - player_name.get_width()//2, vs_position[1] - player_name.get_height())
        boss_name_position = (vs_position[0] + vs.get_width()//2 - boss_name.get_width()//2, vs_position[1] + vs.get_height())

        self.game.screen.blit(vs, vs_position)
        self.game.screen.blit(player_name, player_name_position)
        self.game.screen.blit(boss_name, boss_name_position)