import random
import pygame

from config import BASE_BULLET_FLY_TIME, BASE_DMG, BASE_HEALTH, BASE_IMMORTALITY_AFTER_HIT, BASE_SHOOTING_COOLDOWN, BASE_SHOT_SPEED, BASE_SPEED

class Equipment():
    def __init__(self, player):
        #stats
        #health                   #[0-9]      +300%     together 12
        #dmg                      #[0-2]      +200%     together 3
        #dmg_reduction            #[0-0.6]    -60%      
        #shooting_cooldown        #[0-0.3]    -50%      AS 1/0.6 - 1/0.3 
        #bullet_fly_time          #[0-9.5]     +2000%   together 10.0s
        #shot_speed               #[0-10]     +50%      together 30
        #speed                    #[0-3]      +37.5%    together 11
        #luck                     #[0-0.5]    +50%      together 50%
        #immortality              #[0-1.25]   +125%     together 2.25 

        self.stats = {
            "health": 0,
            "dmg": 0,
            "dmg_reduction": 0,
            "shooting_cooldown": 0,
            "bullet_fly_time": 0,
            "shot_speed": 0,
            "speed": 0,
            "luck": 0,
            "immortality": 0,
        }

        self.max_stats = {
            "health": 9,
            "dmg": 2,
            "dmg_reduction": 0.6,
            "shooting_cooldown": 0.3,
            "bullet_fly_time": 9.5,
            "shot_speed": 10,
            "speed": 4,
            "luck": 0.5,
            "immortality": 1.25
        }

        self.min_stats = {
            "health": -2,
            "dmg": -0.5,
            "dmg_reduction": 0,
            "shooting_cooldown": -0.5,
            "bullet_fly_time": -3,
            "shot_speed": -10,
            "speed": -3,
            "luck": 0,
            "immortality": -0.5
        }

        self.extra_stats = {
            "friendly_ghost": 0,
            "dmg_multiplier": 1,
            "dmg_taken_multiplier": 1
        }

        self.extra_stats_max = {
            "friendly_ghost": 2,
            "dmg_multiplier": 3,
            "dmg_taken_multiplier": 3
        }

        self.player = player

        #background
        self.image = pygame.image.load("resources/other/eq-background.png")
        self.width, self.height = self.image.get_size()
        self.x = (player.game.settings.WIN_WIDTH - self.width) // 2
        self.y = (player.game.settings.WIN_HEIGHT - self.height) // 2

        #items
        self.items = []
        self.first_item_x = self.x + 69
        self.first_item_y = self.y + 65
        self.item_distance = 73
        self.item_size = self.item_distance - 3
        self.item_in_row = 4
        self.item_in_col = 7
        self.items_x = [i for i in range(self.first_item_x, self.first_item_x + self.item_distance * self.item_in_row, self.item_distance )]
        self.items_y = [i for i in range(self.first_item_y, self.first_item_y + self.item_distance * self.item_in_col, self.item_distance )]
        
        #cursor
        self.cursor_size = 4
        self.cursor_image = pygame.image.load("resources/other/eq-cursor.png")
        
        self.cursor_y_offset = 2
        self.cursor_x = self.first_item_x - self.cursor_size
        self.cursor_y = self.first_item_y - self.cursor_size - self.cursor_y_offset

        self.highlighted_item_row = 0
        self.highlighted_item_col = 0
        self.highlighted_item_index = self.highlighted_item_col * self.item_in_row + self.highlighted_item_row

        #big item
        self.big_item_x = self.first_item_x + 736
        self.big_item_y = self.first_item_y
        self.big_item_size = 137
        self.big_item_image = None

        #font
        self.font_path = 'resources/fonts/IsaacGame.ttf'
        self.font_color = (54, 47, 45)

        #stats
        self.stats_x = self.x + 475
        self.stats_y = self.y + 90
        self.stats_y_change = 58

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_items(screen)
        self.draw_item_cursor(screen)
        self.draw_big_item(screen)
        self.draw_player_stats(screen)
    
    def draw_background(self, screen):
        screen.blit(self.image, (self.x, self.y)) 

    def draw_items(self, screen):
        items_drawn = 0
        for item in self.items:
            x = self.items_x[items_drawn % self.item_in_row]
            y = self.items_y[items_drawn // self.item_in_row]

            item_image = pygame.transform.scale(item["image"], (self.item_size, self.item_size))       
            screen.blit(item_image, (x, y))

            items_drawn += 1
            if items_drawn >= self.item_in_row * self.item_in_col:
                return

    def draw_item_cursor(self, screen):
        screen.blit(self.cursor_image, (self.cursor_x, self.cursor_y))

    def draw_big_item(self, screen):
        if self.big_item_image:
            screen.blit(self.big_item_image, (self.big_item_x, self.big_item_y))
            self.draw_item_stats(screen)

    def draw_item_stats(self, screen):
        item = self.items[self.highlighted_item_index]
        x = self.big_item_x + self.big_item_size//2
        y = self.big_item_y + self.big_item_size + self.big_item_size//4
        
        big_font = pygame.font.Font(self.font_path, 33)
        font = pygame.font.Font(self.font_path, 23)
        small_font = pygame.font.Font(self.font_path, 20)

        #item_name
        name_text = item["name"]
        name = big_font.render(name_text, True, self.font_color)
        name_rect = name.get_rect(center=(x, y))
        screen.blit(name, name_rect)

        #item_amount
        amount = small_font.render(str(item["amount"]), True, self.font_color)
        amount_x = self.big_item_x + int(0.9*self.big_item_size) 
        amount_y = self.big_item_y + 10
        amount_rect = amount.get_rect(center=(amount_x, amount_y))
        screen.blit(amount, amount_rect)

        y += self.big_item_size//4
        if "description" in item["stats"].keys():
            description = item["stats"]["description"]
            description_lines = []
            self.prepare_desc_lines(description, description_lines)
            for i, line in enumerate(description_lines):
                description_text = font.render(line, True, self.font_color)
                description_rect = description_text.get_rect(center=(x, y + i * self.big_item_size // 4))
                screen.blit(description_text, description_rect)
    
        else:
            for key, value in item["stats"].items():
                char = "+" if key != "shooting_cooldown" else "-"
                key = key.upper()
                stat = font.render(key.replace("_", " ") + f": {char}{value}", True, self.font_color)
                stat_rect = stat.get_rect(center=(x, y))
                screen.blit(stat, stat_rect)
                y += self.big_item_size//4

    def prepare_desc_lines(self, description, description_lines):
        line = ""
        for word in description.split():
            if len(line) + len(word) <= 25:
                line += word + " "
            else:
                description_lines.append(line.strip())
                line = word + " "
        if line:
            description_lines.append(line.strip())
        


    def draw_player_stats(self, screen):
        x = self.stats_x
        y = self.stats_y

        font = pygame.font.Font(self.font_path, 33)

        for key, value in self.stats.items():
            stat = font.render(f"{value + BASE_HEALTH} / {self.max_stats[key] + BASE_HEALTH}", True, self.font_color)
            if key == "dmg":
                stat = font.render(f"{(value + BASE_DMG):.1f} / {(self.max_stats[key] + BASE_DMG):.1f}", True, self.font_color)
            elif key == "dmg_reduction":
                stat = font.render(f"{int(value * 100)} / {int(self.max_stats[key] * 100)} %", True, self.font_color)
            elif key == "shooting_cooldown":
                stat = font.render(f"{(1/(BASE_SHOOTING_COOLDOWN - value)):.2f} / {(1/(BASE_SHOOTING_COOLDOWN - self.max_stats[key])):.2f}", True, self.font_color)
            elif key == "bullet_fly_time":
                stat = font.render(f"{value + BASE_BULLET_FLY_TIME} / {int(self.max_stats[key] + BASE_BULLET_FLY_TIME)} s", True, self.font_color)
            elif key == "shot_speed":
                stat = font.render(f"{value + BASE_SHOT_SPEED} / {self.max_stats[key] + BASE_SHOT_SPEED}", True, self.font_color)
            elif key == "speed":
                stat = font.render(f"{value + BASE_SPEED} / {self.max_stats[key] + BASE_SPEED}", True, self.font_color)
            elif key == "luck":
                stat = font.render(f"{int(value * 100)} / {int(self.max_stats[key] * 100)} %", True, self.font_color)
            elif key == "immortality":
                stat = font.render(f"{value + BASE_IMMORTALITY_AFTER_HIT} / {self.max_stats[key] + BASE_IMMORTALITY_AFTER_HIT} s", True, self.font_color)
            stat_rect = stat.get_rect(midleft=(x, y))
            screen.blit(stat, stat_rect)
            y += self.stats_y_change


    def user_eq_input(self, event_key):
        if event_key is not None:
            if event_key == pygame.K_DOWN or event_key == pygame.K_s:
                self.highlighted_item_col += 1
                        
            if event_key == pygame.K_UP or event_key == pygame.K_w:
                self.highlighted_item_col -= 1
                        
            if event_key == pygame.K_LEFT or event_key == pygame.K_a:
                self.highlighted_item_row -= 1
                        
            if event_key == pygame.K_RIGHT or event_key == pygame.K_d:
                self.highlighted_item_row += 1
            
            self.highlighted_item_row %= self.item_in_row
            self.highlighted_item_col %= self.item_in_col
        self.set_cursor_and_big_item()
    
    def set_cursor_and_big_item(self):
        self.cursor_x = self.items_x[self.highlighted_item_row] - self.cursor_size
        self.cursor_y = self.items_y[self.highlighted_item_col] - self.cursor_size - self.cursor_y_offset 
        self.highlighted_item_index = self.highlighted_item_col * self.item_in_row + self.highlighted_item_row

        if self.highlighted_item_index >= len(self.items):
            self.big_item_image = None
            return

        self.big_item_image = pygame.transform.scale(self.items[self.highlighted_item_index]["image"], 
                                                    (self.big_item_size, self.big_item_size))

    def add_item(self, item):
        try:
            index = self.items.index(item)
            self.items[index]["amount"] += 1
        except ValueError:
            item["amount"] = 1
            self.items.append(item)

        self.unpack_item(item)

    def use_pill(self, item):
        stats = item["stats"]
        for key, value in stats.items():
            if self.stats.get(key) is not None:
                self.stats[key] += random.choice(value)
                if self.stats[key] > self.max_stats[key]:
                    self.stats[key] = self.max_stats[key]
                if self.stats[key] < self.min_stats[key]:
                    self.stats[key] = self.min_stats[key]

    def unpack_item(self, item):
        stats = item["stats"]
        healValue = 0

        if stats.get("description") is not None:
            for key, value in stats.items():
                if key != "description" and self.extra_stats.get(key) is not None:
                    
                    if key.find("multiplier") != -1:
                        self.extra_stats[key] *= value
                    else:
                        self.extra_stats[key] += value

                    if self.extra_stats[key] > self.extra_stats_max[key]:
                        self.extra_stats[key] = self.extra_stats_max[key]
                    elif key == "friendly_ghost":
                        self.player.spawn_pets(False)
        else:
            for key, value in stats.items():
                if self.stats.get(key) is not None:
                    self.stats[key] += value
                    if self.stats[key] > self.max_stats[key]:
                        self.stats[key] = self.max_stats[key]
                    elif key == "health":
                        healValue = value
            
            self.player.update_player_stats()
            if healValue:
                self.player.heal(healValue)