import pygame

from config import BASE_BULLET_FLY_TIME, BASE_IMMORTALITY_AFTER_HIT, BASE_SHOOTING_COOLDOWN, BASE_SHOT_SPEED

class EquipmentDisplay():
    def __init__(self, equipment, game):
        self.eq = equipment
        self.game = game
        self.player = equipment.player
        #BACKGROUND
        self.image = pygame.image.load("resources/other/eq-background.png")
        self.width, self.height = self.image.get_size()
        self.x = (game.settings.WIN_WIDTH - self.width) // 2
        self.y = (game.settings.WIN_HEIGHT - self.height) // 2

        #ITEMS
        self.first_item_x = self.x + 69
        self.first_item_y = self.y + 65
        self.item_distance = 73
        self.item_size = self.item_distance - 3
        self.item_in_row = 4
        self.item_in_col = 7
        self.items_x = [i for i in range(self.first_item_x, self.first_item_x + self.item_distance * self.item_in_row, self.item_distance )]
        self.items_y = [i for i in range(self.first_item_y, self.first_item_y + self.item_distance * self.item_in_col, self.item_distance )]

        #CURSOR
        self.cursor_size = 4
        self.cursor_image = pygame.image.load("resources/other/eq-cursor.png")
        
        self.cursor_y_offset = 2
        self.cursor_x = self.first_item_x - self.cursor_size
        self.cursor_y = self.first_item_y - self.cursor_size - self.cursor_y_offset

        self.highlighted_item_row = 0
        self.highlighted_item_col = 0
        self.highlighted_item_index = self.highlighted_item_col * self.item_in_row + self.highlighted_item_row

        #BIG_ITEM
        self.big_item_x = self.first_item_x + 736
        self.big_item_y = self.first_item_y
        self.big_item_size = 137
        self.big_item_image = None

        #FONT
        self.font_path = 'resources/fonts/IsaacGame.ttf'
        self.font_path_2 = 'resources/fonts/LuckiestGuy-Regular.ttf'
        self.font_color = (54, 47, 45)

        #STATS
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
        for item in self.eq.items:
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
            self.draw_big_item_stats(screen)
    
    def draw_big_item_stats(self, screen):
        item = self.eq.items[self.highlighted_item_index]
        x = self.big_item_x + self.big_item_size//2
        y = self.big_item_y + self.big_item_size + self.big_item_size//4
        
        small_font = pygame.font.Font(self.font_path, 20)
        big_font_2 = pygame.font.Font(self.font_path_2, 33)
        font_2 = pygame.font.Font(self.font_path_2, 23)

        #item_name
        name_text = item["name"]
        name = big_font_2.render(name_text, True, self.font_color)
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
                description_text = font_2.render(line, True, self.font_color)
                description_rect = description_text.get_rect(center=(x, y + i * self.big_item_size // 4))
                screen.blit(description_text, description_rect)
    
        else:
            for key, value in item["stats"].items():
                char = "+" if key != "shooting_cooldown" else "-"
                stat = font_2.render(key.replace("_", " ") + f": {char}{value}", True, self.font_color)
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
        speed = self.player.speed / self.game.settings.SCALE
        speed = round(speed)
        font = pygame.font.Font(self.font_path, 33)
        stat_formats = {
            "health": f"{self.player.max_health} / {self.eq.max_stats['health'] + self.player.BASE_MAX_HEALTH}",
            "dmg": f"{(self.eq.stats['dmg'] + self.player.dmg):.1f} / {(self.eq.max_stats['dmg'] + self.player.dmg):.1f}",
            "dmg_reduction": f"{int(self.eq.stats['dmg_reduction'] * 100)} / {int(self.eq.max_stats['dmg_reduction'] * 100)} %",
            "shooting_cooldown": f"{(1/(BASE_SHOOTING_COOLDOWN - self.eq.stats['shooting_cooldown'])):.2f} / {(1/(BASE_SHOOTING_COOLDOWN - self.eq.max_stats['shooting_cooldown'])):.2f}",
            "bullet_fly_time": f"{self.eq.stats['bullet_fly_time'] + BASE_BULLET_FLY_TIME} / {int(self.eq.max_stats['bullet_fly_time'] + BASE_BULLET_FLY_TIME)} s",
            "shot_speed": f"{self.eq.stats['shot_speed'] + BASE_SHOT_SPEED} / {self.eq.max_stats['shot_speed'] + BASE_SHOT_SPEED}",
            "speed": f"{self.eq.stats['speed'] + self.player.BASE_SPEED} / {self.eq.max_stats['speed'] + self.player.BASE_SPEED}",
            "luck": f"{int(self.eq.stats['luck'] * 100)} / {int(self.eq.max_stats['luck'] * 100)} %",
            "immortality": f"{self.eq.stats['immortality'] + BASE_IMMORTALITY_AFTER_HIT} / {self.eq.max_stats['immortality'] + BASE_IMMORTALITY_AFTER_HIT} s"
        }

        for key in self.eq.stats:
            stat = font.render(stat_formats[key], True, self.font_color)
            stat_rect = stat.get_rect(midleft=(x, y))
            screen.blit(stat, stat_rect)
            y += self.stats_y_change

    def change_highlighted_item(self, event_key):
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

        if self.highlighted_item_index >= len(self.eq.items):
            self.big_item_image = None
            return
        
        item, size = self.eq.items[self.highlighted_item_index]["image"], (self.big_item_size, self.big_item_size)
        self.big_item_image = pygame.transform.scale(item, size)