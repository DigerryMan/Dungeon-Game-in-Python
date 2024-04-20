import pygame

class ImageLoader:
    def __init__(self):
        self.menu = ["introbackground", "menucard", "settingscard", "menuoverlay", "pausecard2", "arrow2", "maintitle"]
        self._mobs = ["alpha_maggot", "fly","legs", "maggot", "parasite", "slime"]
        self.rooms = ["basement", "catacombs", "caves", "controls", "depths", "necropolis", "shading", "shop", "utero", "womb"]
        self.doors = ["angel_door", "boss_door", "devil_door", "door", "red_door"]
        self.blocks = ["rocks2"]
        self.images_dict = {}
        self.__load_images_to_dict()

    def __load_images_to_dict(self):
        for menu_element in self.menu:
            self.images_dict[menu_element] = pygame.image.load("resources/menu/" + menu_element + ".png")

        for mob in self._mobs:
            self.images_dict[mob] = pygame.image.load("resources/mobs/" + mob + ".png")

        for room in self.rooms:
            self.images_dict[room] = pygame.image.load("resources/rooms/" + room + ".png")

        for door in self.doors:
            self.images_dict[door] = pygame.image.load("resources/doors/" + door + ".png")

        for block in self.blocks:
            self.images_dict[block] = pygame.image.load("resources/blocks/" + block + ".png")

    def get_image(self, name: str):
        return self.images_dict[name]
       
