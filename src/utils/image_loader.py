import pygame

class ImageLoader:
    def __init__(self):
        self._mobs = ["alpha_maggot", "fly","legs", "maggot", "parasite", "slime"]
        self.rooms = ["basement", "catacombs", "caves", "controls", "depths", "necropolis", "shading", "shop", "utero", "womb"]
        self.doors = ["angel_door", "boss_door", "devil_door", "door", "red_door"]
        self.blocks = ["rocks"]
        self._path = "resources/mobs/"
        self._images_dict = {}
        self.__load_images_to_dict()

    def __load_images_to_dict(self):
        for mob in self._mobs:
            self._images_dict[mob] = pygame.image.load(self._path + mob + ".png")

        for room in self.rooms:
            self._images_dict[room] = pygame.image.load(self._path + room + ".png")

        for door in self.doors:
            self._images_dict[door] = pygame.image.load(self._path + door + ".png")

        for block in self.blocks:
            self._images_dict[block] = pygame.image.load(self._path + block + ".png")

    def get_image(self, name: str):
        return self._images_dict[name]
       
