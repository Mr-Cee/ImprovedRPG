import random

import pygame.sprite
from CONFIG import *
from SpriteUtilities import *


class TerrainTemplate(pygame.sprite.Sprite):
    TerrainList = ('Tree', 'Rock')

    def __init__(self, game, pos, group):
        self.game = game
        super().__init__(self.game.all_sprites, self.game.camera_group, group)
        self.image = pygame.image.load('assets/tree.png')  # Defaults to Tree Image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        if not (self.game.player.rect.x - (WIN_WIDTH / 2 + 25)) <= self.rect.x <= (
                self.game.player.rect.x + (WIN_WIDTH / 2 + 25)):
            self.kill()
        elif not (self.game.player.rect.y - (WIN_HEIGHT / 2 + 25)) <= self.rect.y <= (
                self.game.player.rect.y + (WIN_HEIGHT / 2 + 25)):
            self.kill()
        if self.rect.colliderect(self.game.MainTownRect):
            self.kill()

        # print(self.rect)


class Tree(TerrainTemplate):
    def __init__(self, game, pos, group):
        super().__init__(game, pos, group)
        self.image = pygame.image.load('assets/tree.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect(pos[0] + 25, pos[1] + 35, self.image.get_width() - 50,
                                          self.image.get_height() - 45)


class Rock(TerrainTemplate):
    def __init__(self, game, pos, group):
        super().__init__(game, pos, group)
        self.rock_spritesheet = SpriteSheet('assets/rocks.png')
        self.rock1 = self.rock_spritesheet.get_sprite(2, 328, 57, 55)
        self.rock2 = self.rock_spritesheet.get_sprite(131, 325, 60, 58)
        self.rock3 = self.rock_spritesheet.get_sprite(197, 335, 57, 47)
        self.rock4 = self.rock_spritesheet.get_sprite(291, 452, 60, 59)
        self.imageList = [self.rock1, self.rock2, self.rock3, self.rock4]
        randint = random.randint(0, len(self.imageList)-1)
        print(self.imageList[randint])
        self.image = self.imageList[randint]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect(pos[0], pos[1], 64, 64)




