import pygame

from map.block import Block


class EnemyCollisions:
    def __init__(self, enemy, game, check_block_colisions, boss=None):
        self.boss = boss
        self.enemy = enemy
        self.game = game
        self._check_block_colisions = check_block_colisions

    def collide_player(self):
        if not self.enemy._is_dead:
            rect_hits = pygame.sprite.spritecollide(
                self.enemy, self.game.player_sprite, False
            )
            if rect_hits:
                mask_hits = self.enemy.get_mask_colliding_sprite(rect_hits)
                if mask_hits:
                    self.game.damage_player(self.enemy._collision_damage)
                    if self.enemy._is_wandering:
                        self.enemy._is_wandering = False
                        self.enemy.group_attacked()

    def get_mask_colliding_sprite(self, rect_hits):
        for sprite in rect_hits:
            if isinstance(
                sprite, Block
            ):  # done in order to prevent mobs from getting blocked by rough blocks
                block_surface = pygame.Surface((sprite.rect.width, sprite.rect.height))
                block_mask = pygame.mask.from_surface(block_surface)
                offset_x = sprite.rect.x - self.enemy.rect.x
                offset_y = sprite.rect.y - self.enemy.rect.y
                if self.enemy.mask.overlap(block_mask, (offset_x, offset_y)):
                    return sprite

            if pygame.sprite.collide_mask(self.enemy, sprite):
                return sprite

    def collide_blocks(self, orientation: str):
        rect_hits = pygame.sprite.spritecollide(
            self.enemy, self.game.collidables, False
        )
        if rect_hits:
            if self.boss is None:
                mask_hits = self.get_mask_colliding_sprite(rect_hits)
                if mask_hits:
                    self.revert_move(orientation)
            else:
                self.revert_move(orientation)
            
        if self.boss is not None:
            self.collide_beetwen_FlyAggresive(orientation)

    def terrain_collisions(self):
        self.enemy.rect.x += self.enemy.x_change
        if self._check_block_colisions:
            self.collide_blocks("x")

        self.enemy.rect.y += self.enemy.y_change
        if self._check_block_colisions:
            self.collide_blocks("y")

    def revert_move(self, orientation: str):
        if orientation == "x":
            self.enemy.rect.x -= self.enemy.x_change
        elif orientation == "y":
            self.enemy.rect.y -= self.enemy.y_change
    
    def collide_beetwen_FlyAggresive(self, orientation: str):
        rect_hits_enemies = pygame.sprite.spritecollide(self.enemy, self.game.enemies, False)
        try:
            rect_hits_enemies.remove(self.enemy)
            rect_hits_enemies.remove(self.boss)
        except ValueError:
            pass

        if rect_hits_enemies:
            mask_hits = self.get_mask_colliding_sprite(rect_hits_enemies)
            if mask_hits:
                self.revert_move(orientation)