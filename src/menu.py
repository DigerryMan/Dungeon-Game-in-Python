import pygame
from config import FPS

class Menu():
    def __init__(self, game):
        self.game = game
        self.update_images()

    def update_images(self):
        self.intro_background = self.game.image_loader.get_image("introbackground")
        self.menu_card = self.game.image_loader.get_image("menucard")
        self.settings_card = self.game.image_loader.get_image("settingscard")
        self.menu_background = self.game.image_loader.get_image("menuoverlay")
        self.pause_card = self.game.image_loader.get_image("pausecard")
        self.arrow = self.game.image_loader.get_image("arrow")
        self.main_title = self.game.image_loader.get_image("maintitle")

    def intro_screen(self):
        while self.game.intro_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.intro_playing = False
                    self.game.running = False

                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN)):
                    self.game.intro_playing = False
                    self.game.menu_playing = True

            self.game.screen.blit(self.intro_background, (0, 0))
            self.game.clock.tick(FPS)
            pygame.display.update()

    def main_menu(self):
        arrow_positions = [(self.game.settings.WIN_WIDTH//2.35, self.game.settings.WIN_HEIGHT//3.13), 
                           (self.game.settings.WIN_WIDTH//2.44, self.game.settings.WIN_HEIGHT//2.15), 
                           (self.game.settings.WIN_WIDTH//2.27, self.game.settings.WIN_HEIGHT//1.67)]
        current_arrow = 0

        while self.game.menu_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.menu_playing = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        current_arrow = current_arrow + 1 if current_arrow < 2 else 0

                    if event.key == pygame.K_UP:
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 2

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.game.menu_playing = False
                            self.game.render_new_map(first_map = True)
                            self.game.paused = False

                        elif current_arrow == 1:
                            self.game.menu_playing = False
                            self.game.settings_playing = True
                            self.display_settings()
                            arrow_positions = [(self.game.settings.WIN_WIDTH//2.35, self.game.settings.WIN_HEIGHT//3.13), 
                                            (self.game.settings.WIN_WIDTH//2.44, self.game.settings.WIN_HEIGHT//2.15), 
                                            (self.game.settings.WIN_WIDTH//2.27, self.game.settings.WIN_HEIGHT//1.67)]
                            
                            if not self.game.menu_playing:
                                return

                        elif current_arrow == 2:
                            self.game.menu_playing = False
                            self.game.running = False

            self.game.screen.blit(self.menu_card, (0, 0))
            self.game.screen.blit(self.menu_background, (0, 0))
            self.game.screen.blit(self.main_title, (self.game.settings.WIN_WIDTH//8, 0))

            self.game.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.game.clock.tick(FPS)
            pygame.display.update()

    def display_settings(self):
        settings_playing = True
        arrow_positions = None

        def get_arrow_positions():
            nonlocal arrow_positions
            arrow_positions = [(self.game.settings.WIN_WIDTH//2.52, self.game.settings.WIN_HEIGHT//2.78), 
                        (self.game.settings.WIN_WIDTH//2.48, self.game.settings.WIN_HEIGHT//2.13), 
                        (self.game.settings.WIN_WIDTH//2.43, self.game.settings.WIN_HEIGHT//1.72)]
            
        get_arrow_positions()
        current_arrow = 0

        while settings_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    settings_playing = False
                    self.game.menu_playing = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        current_arrow = current_arrow + 1 if current_arrow < 2 else 0

                    if event.key == pygame.K_UP:
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 2

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.window_size = (1920, 1080)

                        elif current_arrow == 1:
                            self.window_size = (1600, 900)

                        elif current_arrow == 2:
                            self.window_size = (1280, 720)
                        
                        self.game.handle_resolution_change(self.window_size)
                        get_arrow_positions()

                    if event.key == pygame.K_ESCAPE:
                        settings_playing = False
                        self.game.menu_playing = True


            self.game.screen.blit(self.settings_card, (0, 0))
            self.game.screen.blit(self.menu_background, (0, 0))
            self.game.screen.blit(self.main_title, (self.game.settings.WIN_WIDTH//8, 0))

            self.game.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.game.clock.tick(FPS)
            pygame.display.update()

    def display_pause(self):
        arrow_positions = [(self.game.settings.WIN_WIDTH//3.1, self.game.settings.WIN_HEIGHT//2.05),
                           (self.game.settings.WIN_WIDTH//2.85, self.game.settings.WIN_HEIGHT//1.75)]
        current_arrow = 0

        while self.game.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.paused = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.paused = False
                    
                    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        current_arrow = current_arrow + 1 if current_arrow == 0 else 0

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.game.paused = False
                        elif current_arrow == 1:
                            self.game.paused = False
                            self.game.menu_playing = True

            self.game.screen.blit(self.pause_card, (self.game.settings.WIN_WIDTH//4, self.game.settings.WIN_HEIGHT//4))
            self.game.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.game.clock.tick(FPS)
            pygame.display.update()