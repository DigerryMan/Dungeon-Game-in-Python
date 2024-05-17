import pygame
from config import FPS
from entities.player.player_types import PlayerTypes

class Menu():
    def __init__(self, game):
        self.game = game
        self.update_images()

    def update_images(self):
        self.intro_background = self.game.image_loader.get_image("introbackground")
        self.menu_card = self.game.image_loader.get_image("menucard")
        self.settings_card = self.game.image_loader.get_image("settingscard")
        self.character_selection = self.game.image_loader.get_image("character_selection")
        self.menu_background = self.game.image_loader.get_image("menuoverlay")
        self.pause_card = self.game.image_loader.get_image("pausecard")
        self.arrow = self.game.image_loader.get_image("arrow")
        self.main_title = self.game.image_loader.get_image("maintitle")

    def intro_screen(self):
        self.game.sound_manager.play_with_fadein("intro", 2000, looped=True)
        while self.game.intro_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.intro_playing = False
                    self.game.running = False

                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN)):
                    self.game.sound_manager.stop_with_fadeout("intro", 2000)
                    self.game.intro_playing = False
                    self.game.menu_playing = True

            self.game.screen.blit(self.intro_background, (0, 0))
            self.game.clock.tick(FPS)
            pygame.display.update()

    def main_menu(self):
        self.game.sound_manager.play_with_fadein("menuMusic", 2000, looped=True)
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
                        self.game.sound_manager.play("selectLeft")

                    if event.key == pygame.K_UP:
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 2
                        self.game.sound_manager.play("selectRight")

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.game.sound_manager.play("pageTurn")
                            self.game.menu_playing = False
                            self.display_character_selection()
                            self.game.paused = False

                        elif current_arrow == 1:
                            self.game.sound_manager.play("pageTurn")
                            self.game.menu_playing = False
                            self.display_settings()
                            arrow_positions = [(self.game.settings.WIN_WIDTH//2.35, self.game.settings.WIN_HEIGHT//3.13), 
                                            (self.game.settings.WIN_WIDTH//2.44, self.game.settings.WIN_HEIGHT//2.15), 
                                            (self.game.settings.WIN_WIDTH//2.27, self.game.settings.WIN_HEIGHT//1.67)]
                            
                        elif current_arrow == 2:
                            self.game.menu_playing = False
                            self.game.running = False

                        if not self.game.menu_playing:
                            self.game.sound_manager.stop_with_fadeout("menuMusic", 2000)
                            return

            self.game.screen.blit(self.menu_card, (0, 0))
            self.game.screen.blit(self.menu_background, (0, 0))
            self.game.screen.blit(self.main_title, (self.game.settings.WIN_WIDTH//8, 0))

            self.game.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.game.clock.tick(FPS)
            pygame.display.update()

    def display_character_selection(self):
        character_selection_playing = True
        characters = PlayerTypes.get_all_characters()
        current_character = 0

        image, name, stats = None, None, None

        def set_character_display():
            nonlocal image, name, stats
            image = self.game.image_loader.images_dict[characters[current_character].value + "_display"]["image"]
            name = self.game.image_loader.images_dict[characters[current_character].value + "_display"]["name"]
            stats = self.game.image_loader.images_dict[characters[current_character].value + "_display"]["stats"]

        set_character_display()

        while character_selection_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    character_selection_playing = False
                    self.game.menu_playing = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.game.sound_manager.play("selectRight")
                        current_character = (current_character + 1) % len(characters)
                        set_character_display()

                    if event.key == pygame.K_LEFT:
                        self.game.sound_manager.play("selectLeft")
                        current_character = (current_character - 1) % len(characters)
                        set_character_display()

                    if event.key == pygame.K_RETURN:
                        self.game.sound_manager.play("pageTurn")
                        character_selection_playing = False
                        self.game.character_type = characters[current_character]
                        self.game.render_new_map(first_map = True)

                    if event.key == pygame.K_ESCAPE:
                        self.game.sound_manager.play("pageTurn")
                        character_selection_playing = False
                        self.game.menu_playing = True

            self.game.screen.blit(self.character_selection, (0, 0))
            self.game.screen.blit(image, (self.game.settings.WIN_WIDTH//2.25, self.game.settings.WIN_HEIGHT//2.5))
            self.game.screen.blit(name, (self.game.settings.WIN_WIDTH//2.25, self.game.settings.WIN_HEIGHT//1.8))
            self.game.screen.blit(stats, (self.game.settings.WIN_WIDTH//2.5, self.game.settings.WIN_HEIGHT//1.5))
            self.game.screen.blit(self.menu_background, (0, 0))
            self.game.screen.blit(self.main_title, (self.game.settings.WIN_WIDTH//8, 0))

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
                        self.game.sound_manager.play("selectLeft")
                        current_arrow = current_arrow + 1 if current_arrow < 2 else 0

                    if event.key == pygame.K_UP:
                        self.game.sound_manager.play("selectRight")
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 2

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.window_size = (1920, 1080)

                        elif current_arrow == 1:
                            self.window_size = (1600, 900)

                        elif current_arrow == 2:
                            self.window_size = (1280, 720)

                        self.game.sound_manager.play("steam")
                        
                        self.game.handle_resolution_change(self.window_size)
                        get_arrow_positions()

                    if event.key == pygame.K_ESCAPE:
                        self.game.sound_manager.play("pageTurn")
                        settings_playing = False
                        self.game.menu_playing = True


            self.game.screen.blit(self.settings_card, (0, 0))
            self.game.screen.blit(self.menu_background, (0, 0))
            self.game.screen.blit(self.main_title, (self.game.settings.WIN_WIDTH//8, 0))

            self.game.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.game.clock.tick(FPS)
            pygame.display.update()

    def display_pause(self):
        self.game.sound_manager.play("pageTurn")
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
                        self.game.sound_manager.play("pageTurn")
                        self.game.paused = False
                    
                    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        current_arrow = current_arrow + 1 if current_arrow == 0 else 0
                        self.game.sound_manager.play("selectRight")

                    if event.key == pygame.K_RETURN:
                        if current_arrow == 0:
                            self.game.paused = False
                            self.game.sound_manager.play("pageTurn")
                        elif current_arrow == 1:
                            self.game.paused = False
                            self.game.menu_playing = True
                            self.game.sound_manager.play("pageTurn")

            self.game.screen.blit(self.pause_card, (self.game.settings.WIN_WIDTH//4, self.game.settings.WIN_HEIGHT//4))
            self.game.screen.blit(self.arrow, (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]))

            self.game.clock.tick(FPS)
            pygame.display.update()