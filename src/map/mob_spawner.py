import random
from entities.mobs.alpha_maggot import AlphaMaggot
from entities.mobs.boss.duke.duke import Duke
from entities.mobs.boss.forsaken.forsaken import Forsaken
from entities.mobs.boss.husk.husk import Husk
from entities.mobs.boss.monstro.monstro import Monstro
from entities.mobs.boss.monstro.monstro2 import Monstro2
from entities.mobs.boss.satan.satan import Satan
from entities.mobs.boss.satan.satan2 import Satan2
from entities.mobs.fly import Fly
from entities.mobs.ghost import Ghost
from entities.mobs.legs import Legs
from entities.mobs.maggot import Maggot
from entities.mobs.parasite import Parasite
from entities.mobs.slime import Slime
from entities.mobs.wanderer import Wanderer
from utils.directions import Directions


class MobSpawner():
    def __init__(self, room, game):
        self.game = game
        self.room = room
        self.mob_spawn_positions = []
        self.mobs_amount = 2 + room.level // 2
    
    def spawn_mobs(self):
        self.mobs_amount = min(self.mobs_amount, len(self.mob_spawn_positions))
        self.mob_spawn_positions = random.sample(self.mob_spawn_positions, self.mobs_amount)

        mobs = [Legs, Parasite, AlphaMaggot, Fly, Ghost, Maggot, Slime, Wanderer]
        index = random.randint(0, len(mobs) - 1)

        if self.room.room_type == "boss":
            match self.room.level:
                case 1:
                    self.room.enemies.append(Duke(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))
                case 2:
                    self.room.enemies.append(Monstro(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))
                case 3:
                    self.room.enemies.append(Husk(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))
                case 4:
                    self.room.enemies.append(Satan(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))
                case 5:
                    self.room.enemies.append(Forsaken(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))
                case 6:
                    self.room.enemies.append(Monstro2(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))
                case 7:
                    self.room.enemies.append(Satan2(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))

            return

        for (y, x) in self.mob_spawn_positions:
            new_mob = mobs[index]
            self.room.enemies.append(new_mob(self.game, x, y))
            index = random.randint(0, len(mobs) - 1)
            break # ADDED FOR ONLY 1 MOB TO SPAWN
    
    def spawn_mob(self, mob_class, x, y, boss=None):
        if boss:
            self.room.enemies.append(mob_class(self.game, x, y, boss))
        else:
            self.room.enemies.append(mob_class(self.game, x, y))
    
    def spawn_player(self, entry_direction, game):
        if entry_direction == Directions.UP:
            game.player.rect.center = (game.settings.WIN_WIDTH // 2, (game.settings.MAP_HEIGHT - 2) * game.settings.TILE_SIZE + game.settings.PLAYER_SIZE * 0.9)
        elif entry_direction == Directions.DOWN:
            game.player.rect.center = (game.settings.WIN_WIDTH // 2, game.settings.TILE_SIZE * 1.1)
        elif entry_direction == Directions.LEFT:
            game.player.set_rect_position((game.settings.MAP_WIDTH - 2) * game.settings.TILE_SIZE + (game.settings.TILE_SIZE - game.settings.PLAYER_SIZE), 
                                          game.player.rect.y)
        elif entry_direction == Directions.RIGHT:
            game.player.set_rect_position(game.settings.TILE_SIZE - (game.settings.TILE_SIZE - game.settings.PLAYER_SIZE),
                                          game.player.rect.y)
        elif entry_direction == Directions.CENTER:
            game.player.rect.center = (game.settings.WIN_WIDTH // 2, game.settings.WIN_HEIGHT // 2)
