import pygame
import config


class Equipment():
    def __init__(self, player):
        #stats
        #health                   #[0-9]      +300%     together 12
        #dmg_reduction            #[0-0.6]    -60%      
        #dmg                      #[0-2]      +200%     together 3
        #speed                    #[0-3]      +37.5%    together 11
        #extra_immortality        #[0-1.25]   +125%     together 2.25 
        #shooting_cd_decrease     #[0-0.3]    -50%      AS 1/0.6 - 1/0.3 
        #shot_speed               #[0-10]     +50%      together 30
        #luck                     #[0-0.5]    +50%      together 50%

        self.stats = {
            "health": 0,
            "dmg": 0,
            "dmg_reduction": 0,
            "shooting_cd_decrease": 0,
            "bullet_fly_time": 0,
            "shot_speed": 0,
            "speed": 0,
            "luck": 0,
            "extra_immortality": 0
        }

        self.max_stats = {
            "health": 9,
            "dmg": 2,
            "dmg_reduction": 0.6,
            "shooting_cd_decrease": 0.3,
            "bullet_fly_time": 10,
            "shot_speed": 10,
            "speed": 3,
            "luck": 0.5,
            "extra_immortality": 1.25
        }

        self.player = player

        #background
        self.image = pygame.image.load("resources/other/eq-background.png")
        self.width, self.height = self.image.get_size()
        self.x = (player.game.settings.WIN_WIDTH - self.width) // 2
        self.y = (player.game.settings.WIN_HEIGHT - self.height) // 2

        #items
        self.items = []
        self.first_item_x = self.x + 22
        self.first_item_y = self.y + 22
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
        self.font_path = 'resources/fonts/LuckiestGuy-Regular.ttf'
        self.font_color = (54, 47, 45)

        #stats
        self.stats_x = self.x + 430
        self.stats_y = self.y + 46
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
        font = pygame.font.Font(self.font_path, 26)
        small_font = pygame.font.Font(self.font_path, 20)

        #item_name
        name = big_font.render(item["name"], True, self.font_color)
        name_rect = name.get_rect(center=(x, y))
        screen.blit(name, name_rect)

        #item_amount
        amount = small_font.render(str(item["amount"]), True, self.font_color)
        amount_x = self.big_item_x + int(0.9*self.big_item_size) 
        amount_y = self.big_item_y + 10
        amount_rect = amount.get_rect(center=(amount_x, amount_y))
        screen.blit(amount, amount_rect)

        #item_stats
        for key, value in item["stats"].items():
            y += self.big_item_size//4
            stat = font.render(f"{key}: +{value}", True, self.font_color)
            stat_rect = stat.get_rect(center=(x, y))
            screen.blit(stat, stat_rect)
        
        #y += self.big_item_size//4

    def draw_player_stats(self, screen):
        x = self.stats_x
        y = self.stats_y

        big_font = pygame.font.Font(self.font_path, 33)
        font = pygame.font.Font(self.font_path, 33)
        small_font = pygame.font.Font(self.font_path, 20)

        
        for key, value in self.stats.items():
            stat = font.render(f"{value} / {self.max_stats[key]}", True, self.font_color)
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

    def unpack_item(self, item):
        stats = item["stats"]
        healValue = 0
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