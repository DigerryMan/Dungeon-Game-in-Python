import pygame

class ImageLoader:
    def __init__(self, settings):
        self.settings = settings
        self.tile_size_tuple = (self.settings.TILE_SIZE, self.settings.TILE_SIZE)

        self.menu_ = ["introbackground", "menucard", "settingscard", "menuoverlay", "pausecard", "arrow", "maintitle"]
        self.mobs_ = ["player", "alpha_maggot", "fly", "legs", "maggot", "parasite", "slime", "wanderer", "ghost", "friend_ghost", "slime_shadow"]
        self.rooms_ = ["controls", "shading", "shop_room", "basement", "cave"]
        self.doors_ = ["boss_door", "devil_door", "basement_door1", "red_door"]
        self.blocks_ = ["rocks"]

        self.images_dict = {}
        self.load_images_to_dict()
        self.scale_menu_images()

        self.blocks = {}
        self.load_blocks()

        self.tears = {}
        self.load_tears()

        self.bombs = {}
        self.load_bombs()

        self.doors = {}
        self.load_doors()

        self.trap_door = {}
        self.load_trap_door()

        self.lootables = {}
        self.load_lootables()

        self.chests = {}
        self.load_chests()

        self.stat_bar = {}
        self.load_stat_bar()

        self.minimap = {}
        self.load_minimap()

        self.player_animation = {}
        self.load_player_animation()

    def load_images_to_dict(self):
        for menu_element in self.menu_:
            self.images_dict[menu_element] = pygame.image.load("resources/menu/" + menu_element + ".png")

        for mob in self.mobs_:
            img = pygame.image.load("resources/mobs/" + mob + ".png").convert_alpha()
            frames_in_row, frames_in_col = img.get_width()/32, img.get_height()/32
            size = self.settings.MOB_SIZE
            if mob == "player":
                size = self.settings.PLAYER_SIZE
            new_size = (frames_in_row * size), (frames_in_col * size)
            self.images_dict[mob] = pygame.transform.scale(img, new_size)
       
        room_scaled_size = (self.settings.WIN_WIDTH * 1.08, self.settings.WIN_HEIGHT * 1.12)
        for room in self.rooms_:
            if room == "controls":
                original_image = pygame.image.load("resources/rooms/" + room + ".png").convert_alpha()
                new_size = (int(original_image.get_width() * self.settings.SCALE), int(original_image.get_height() * self.settings.SCALE))
                self.images_dict[room] = pygame.transform.scale(original_image, new_size)
                continue

            elif room == "basement":
                for i in range(1, 5):
                    self.images_dict[room + str(i)] = pygame.transform.scale(pygame.image.load("resources/rooms/basement/" + room + str(i) + ".png"), room_scaled_size).convert_alpha()

            elif room == "cave":
                for i in range(1, 6):
                    self.images_dict[room + str(i)] = pygame.transform.scale(pygame.image.load("resources/rooms/cave/" + room + str(i) + ".png"), room_scaled_size).convert_alpha()

            else:
                self.images_dict[room] = pygame.transform.scale(pygame.image.load("resources/rooms/" + room + ".png"), room_scaled_size).convert_alpha()

        for door in self.doors_:
            self.images_dict[door] = pygame.image.load("resources/doors/" + door + ".png").convert_alpha()

        for block in self.blocks_:
            self.images_dict[block] = pygame.image.load("resources/blocks/" + block + ".png").convert_alpha()

        self.images_dict["items"] = pygame.image.load("resources/items/items.png").convert_alpha()
        self.images_dict["bullet"] = pygame.image.load("resources/other/tears.png").convert_alpha()
        self.images_dict["tears"] = pygame.image.load("resources/other/tears.png")
        self.images_dict["tears_pop"] = pygame.image.load("resources/other/tears_pop.png")
        self.images_dict["bombs"] = pygame.image.load("resources/other/bombs.png")
        self.images_dict["explosion"] = pygame.image.load("resources/other/explosion.png")
        self.images_dict["trap_door"] = pygame.image.load("resources/other/trap_door.png")
        self.images_dict["gold_coin"] = pygame.image.load("resources/other/penny.png")
        self.images_dict["silver_coin"] = pygame.image.load("resources/other/nickel.png")
        self.images_dict["hearts"] = pygame.image.load("resources/items/pickup_hearts.png")
        self.images_dict["pills"] = pygame.image.load("resources/items/pills.png")
        self.images_dict["small_chest"] = pygame.image.load("resources/other/small_chest.png")
        self.images_dict["medium_chest"] = pygame.image.load("resources/other/medium_chest.png")
        self.images_dict["large_chest"] = pygame.image.load("resources/other/large_chest.png")
        self.images_dict["minimap"] = pygame.image.load("resources/other/minimap.png")

    def scale_menu_images(self):
        screen_size = (self.settings.WIN_WIDTH, self.settings.WIN_HEIGHT)
        self.images_dict["introbackground"] = pygame.transform.scale(self.images_dict["introbackground"], screen_size).convert_alpha()
        self.images_dict["menucard"] = pygame.transform.scale(self.images_dict["menucard"], screen_size).convert_alpha()
        self.images_dict["settingscard"] = pygame.transform.scale(self.images_dict["settingscard"], screen_size).convert_alpha()
        self.images_dict["menuoverlay"] = pygame.transform.scale(self.images_dict["menuoverlay"], screen_size).convert_alpha()
        
        self.images_dict["pausecard"] = pygame.transform.scale(self.images_dict["pausecard"],
                                                                (self.images_dict["pausecard"].get_width() * self.settings.SCALE, self.images_dict["pausecard"].get_height() * self.settings.SCALE)).convert_alpha()
        
        self.images_dict["arrow"] = pygame.transform.scale(self.images_dict["arrow"],
                                                            (self.images_dict["arrow"].get_width() * 0.7 * self.settings.SCALE, self.images_dict["arrow"].get_height() * 0.7 * self.settings.SCALE)).convert_alpha()
        
        self.images_dict["maintitle"] = pygame.transform.scale(self.images_dict["maintitle"],
                                                               (self.images_dict["maintitle"].get_width() * 2.8 * self.settings.SCALE, self.images_dict["maintitle"].get_height() * 2.8 * self.settings.SCALE)).convert_alpha()

    def load_blocks(self):
        self.blocks["rock1"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(5, 5, 51, 55)), self.tile_size_tuple).convert_alpha()
        self.blocks["rock2"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(67, 5, 55, 57)), self.tile_size_tuple).convert_alpha()
        self.blocks["rock3"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(131, 1, 55, 63)), self.tile_size_tuple).convert_alpha()
        self.blocks["rock4"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(69, 133, 51, 56)), self.tile_size_tuple).convert_alpha()

        self.blocks["treasure_rock1"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(69, 69, 51, 55)), self.tile_size_tuple).convert_alpha()
        self.blocks["treasure_rock2"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(197, 135, 53, 55)), self.tile_size_tuple).convert_alpha()

        self.blocks["vase1"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(129, 67, 57, 55)), self.tile_size_tuple).convert_alpha()
        self.blocks["vase2"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(129, 131, 57, 55)), self.tile_size_tuple).convert_alpha()
        self.blocks["vase3"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(133, 195, 49, 55)), self.tile_size_tuple).convert_alpha()
        self.blocks["vase4"] = pygame.transform.scale(self.images_dict["rocks"].subsurface(pygame.Rect(197, 195, 49, 55)), self.tile_size_tuple).convert_alpha()

    def load_tears(self):
        self.tears["blue_tear"] = pygame.transform.scale(self.images_dict["tears"].subsurface(pygame.Rect(650, 12, 42, 42)), (self.settings.BULLET_SIZE, self.settings.BULLET_SIZE)).convert_alpha()
        self.tears["red_tear"] = pygame.transform.scale(self.images_dict["tears"].subsurface(pygame.Rect(650, 76, 42, 42)), (self.settings.BULLET_SIZE, self.settings.BULLET_SIZE)).convert_alpha()

        for i in range(16):
            self.tears["blue_tear_pop" + str(i)] = pygame.transform.scale(self.images_dict["tears_pop"].subsurface(pygame.Rect(i * 64, 0, 64, 64)), (self.settings.BULLET_SIZE*3, self.settings.BULLET_SIZE*3)).convert_alpha()
            self.tears["red_tear_pop" + str(i)] = pygame.transform.scale(self.images_dict["tears_pop"].subsurface(pygame.Rect(i * 64, 64, 64, 64)), (self.settings.BULLET_SIZE*3, self.settings.BULLET_SIZE*3)).convert_alpha()

    def load_bombs(self):
        for i in range(4):
            self.bombs[f"bomb{i}"] = pygame.transform.scale(self.images_dict["bombs"].subsurface(pygame.Rect(i * 32, 160, 32, 32)), self.tile_size_tuple).convert_alpha()

        for i in range(12):
            self.bombs[f"bomb_explosion{i}"] = pygame.transform.scale(self.images_dict["explosion"].subsurface(pygame.Rect((i % 4) * 96, (i // 4) * 96, 96, 96)),
                                                                      (self.settings.TILE_SIZE * 2.5, self.settings.TILE_SIZE * 2.5)).convert_alpha()

    def load_doors(self):
        for i in range(19):
            self.doors[f"basement_door1_{i}"] = pygame.transform.scale(self.images_dict["basement_door1"].subsurface(pygame.Rect(i * 49, 0, 49, 33)), (self.settings.TILE_SIZE * 1.3, self.settings.TILE_SIZE * 1.3)).convert_alpha()

        for i in range(11):
            self.doors[f"boss_door_{i}"] = pygame.transform.scale(self.images_dict["boss_door"].subsurface(pygame.Rect(i * 49, 0, 49, 33)), (self.settings.TILE_SIZE * 1.3, self.settings.TILE_SIZE * 1.3)).convert_alpha()

    def load_trap_door(self):
        self.trap_door["opened"] = pygame.transform.scale(self.images_dict["trap_door"].subsurface(pygame.Rect(16, 16, 32, 32)), self.tile_size_tuple).convert_alpha()
        self.trap_door["closed"] = pygame.transform.scale(self.images_dict["trap_door"].subsurface(pygame.Rect(16, 80, 32, 32)), self.tile_size_tuple).convert_alpha()

    def load_lootables(self):
        size_to_scale = (self.settings.TILE_SIZE * 1.5, self.settings.TILE_SIZE * 1.5)
        for i in range(6):
            self.lootables["gold_coin_shine" + str(i)] = pygame.transform.scale(self.images_dict["gold_coin"].subsurface(pygame.Rect(i * 64, 0, 64, 64)), size_to_scale).convert_alpha()
            self.lootables["silver_coin_shine" + str(i)] = pygame.transform.scale(self.images_dict["silver_coin"].subsurface(pygame.Rect(i * 64, 0, 64, 64)), size_to_scale).convert_alpha()

        for i in range(8):
            self.lootables["gold_coin_drop" + str(i)] = pygame.transform.scale(self.images_dict["gold_coin"].subsurface(pygame.Rect(i * 64, 64, 64, 64)), size_to_scale).convert_alpha()
            self.lootables["silver_coin_drop" + str(i)] = pygame.transform.scale(self.images_dict["silver_coin"].subsurface(pygame.Rect(i * 64, 64, 64, 64)), size_to_scale).convert_alpha()

        for i in range(9):
            self.lootables["gold_coin_pickup" + str(i)] = pygame.transform.scale(self.images_dict["gold_coin"].subsurface(pygame.Rect(i * 64, 128, 64, 64)), size_to_scale).convert_alpha()

        self.lootables["full_heart"] = pygame.transform.scale(self.images_dict["hearts"].subsurface(pygame.Rect(0, 0, 32, 32)), (size_to_scale[0] // 1.8, size_to_scale[1] // 1.8)).convert_alpha()
        self.lootables["half_heart"] = pygame.transform.scale(self.images_dict["hearts"].subsurface(pygame.Rect(32, 0, 32, 32)), (size_to_scale[0] // 1.8, size_to_scale[1] // 1.8)).convert_alpha()

        size_to_scale = (self.settings.TILE_SIZE, self.settings.TILE_SIZE)

        self.lootables["speed_pill"] = pygame.transform.scale(self.images_dict["pills"].subsurface(pygame.Rect(0, 0, 32, 32)), size_to_scale).convert_alpha()
        self.lootables["health_pill"] = pygame.transform.scale(self.images_dict["pills"].subsurface(pygame.Rect(32, 32, 32, 32)), size_to_scale).convert_alpha()
        self.lootables["bullet_fly_time_pill"] = pygame.transform.scale(self.images_dict["pills"].subsurface(pygame.Rect(32, 0, 32, 32)), size_to_scale).convert_alpha()
        self.lootables["dmg_reduction_pill"] = pygame.transform.scale(self.images_dict["pills"].subsurface(pygame.Rect(64, 64, 32, 32)), size_to_scale).convert_alpha()
        self.lootables["dmg_pill"] = pygame.transform.scale(self.images_dict["pills"].subsurface(pygame.Rect(0, 64, 32, 32)), size_to_scale).convert_alpha()
        self.lootables["shooting_cooldown_pill"] = pygame.transform.scale(self.images_dict["pills"].subsurface(pygame.Rect(32, 64, 32, 32)), size_to_scale).convert_alpha()
        self.lootables["shot_speed_pill"] = pygame.transform.scale(self.images_dict["pills"].subsurface(pygame.Rect(64, 0, 32, 32)), size_to_scale).convert_alpha()
        self.lootables["luck_pill"] = pygame.transform.scale(self.images_dict["pills"].subsurface(pygame.Rect(0, 32, 32, 32)), size_to_scale).convert_alpha()
        self.lootables["immortality_pill"] = pygame.transform.scale(self.images_dict["pills"].subsurface(pygame.Rect(64, 32, 32, 32)), size_to_scale).convert_alpha()

    def load_chests(self):
        for i in range(8):
            self.chests[f"small_chest{i}"] = pygame.transform.scale(self.images_dict["small_chest"].subsurface(pygame.Rect(i * 32, 0, 32, 32)), self.tile_size_tuple).convert_alpha()
            self.chests[f"medium_chest{i}"] = pygame.transform.scale(self.images_dict["medium_chest"].subsurface(pygame.Rect(i * 32, 0, 32, 32)), self.tile_size_tuple).convert_alpha()
            self.chests[f"large_chest{i}"] = pygame.transform.scale(self.images_dict["large_chest"].subsurface(pygame.Rect(i * 32, 0, 32, 32)), self.tile_size_tuple).convert_alpha()

    def load_stat_bar(self):
        images = ["coin", "bomb", "empty_heart", "full_heart", "half_heart"]
        for image in images:
            self.stat_bar[image] = pygame.image.load(f"resources/stat_bar/{image}.png").convert_alpha()
            self.stat_bar[image] = pygame.transform.scale(self.stat_bar[image], (self.settings.STAT_BARS_HEALTH_SIZE, self.settings.STAT_BARS_HEALTH_SIZE))

        bar_images = ["full_bar", "empty_bar", "boss_full_bar", "boss_empty_bar"]
        for image in bar_images:
            self.stat_bar[image] = pygame.image.load(f"resources/stat_bar/{image}.png").convert_alpha()

    def get_stat_bar_image(self, name:str):
        return self.stat_bar[name]
    
    def load_minimap(self):
        background_size = (self.images_dict["minimap"].subsurface(pygame.Rect(0, 0, 101, 81)).get_width() * self.settings.SCALE * 2,
                            self.images_dict["minimap"].subsurface(pygame.Rect(0, 0, 101, 81)).get_height() * self.settings.SCALE * 2)
                                                                  
        cell_size = (self.images_dict["minimap"].subsurface(pygame.Rect(111, 0, 19, 15)).get_width() * self.settings.SCALE * 2,
                            self.images_dict["minimap"].subsurface(pygame.Rect(111, 0, 19, 15)).get_height() * self.settings.SCALE * 2)

        self.minimap["background"] = pygame.transform.scale(self.images_dict["minimap"].subsurface(pygame.Rect(0, 0, 101, 81)), background_size).convert_alpha()
        self.minimap["current_room"] = pygame.transform.scale(self.images_dict["minimap"].subsurface(pygame.Rect(111, 0, 19, 15)), cell_size).convert_alpha()
        self.minimap["discovered_room"] = pygame.transform.scale(self.images_dict["minimap"].subsurface(pygame.Rect(111, 15, 19, 15)), cell_size).convert_alpha()
        self.minimap["undiscovered_room"] = pygame.transform.scale(self.images_dict["minimap"].subsurface(pygame.Rect(111, 30, 19, 15)), cell_size).convert_alpha()
        self.minimap["shop_icon"] = pygame.transform.scale(self.images_dict["minimap"].subsurface(pygame.Rect(111, 45, 19, 15)), cell_size).convert_alpha()
        self.minimap["boss_icon"] = pygame.transform.scale(self.images_dict["minimap"].subsurface(pygame.Rect(111, 60, 19, 15)), cell_size).convert_alpha()

    def load_player_animation(self):
        img = pygame.image.load(f"resources/mobs/player.png")
        frame_names = ["die2", "like0", "like1", "die4", 
                       "die0", "pick", "die3", "bad1",
                       "die1", "sit", "happy0", "happy1"]
        index = 0
        for y in range(2, 5):
            for x in range(4):
               sub_img = img.subsurface(pygame.Rect(x * 64, y * 64, 64, 64))
               new_size = int(1.95*self.settings.PLAYER_SIZE), int(1.95*self.settings.PLAYER_SIZE)
               self.player_animation[frame_names[index]] = pygame.transform.scale(sub_img, new_size).convert_alpha()
               index += 1

    def get_image(self, name: str):
        return self.images_dict[name]