import math
import random
from random import randint

import pygame

from CONFIG import *
from SpriteUtilities import SpriteSheet
from Terrain import Tree


class Character(pygame.sprite.Sprite):
    def __init__(self, game, pos):

        self.game = game
        self.screen = self.game.screen
        # super().__init__(self.game.camera_group)

        # Player Attributes
        self.baseHP = 100
        self.maxHP = self.baseHP
        self.hp = self.maxHP

        self.inTown = False
        self.MaxTerrain = 20

        self.width = 64
        self.height = 64
        self.collision_x_offset = 20
        self.collision_y_offset = 40
        self.collision_width_offset = 40
        self.collision_height_offset = 40

        self.x_change = 0
        self.y_change = 0
        self.direction = pygame.math.Vector2()
        self.movement_loop = 0

        self.facing = 'down'
        self.animation_loop = 1
        self.animation_loop_speed = 0.5

        self.character_spritesheet = SpriteSheet('assets/CharacterWalkingSpritesheet.png')
        self.image = self.character_spritesheet.get_sprite(0, 192, self.width, self.height)
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect(self.rect.left + self.collision_x_offset, self.rect.top + self.collision_y_offset, self.width - self.collision_width_offset, self.height - self.collision_height_offset)
        # self.collision_rect = pygame.Rect(100, 100, self.width, self.height)

        self.down_animations = [
            self.character_spritesheet.get_sprite(0, 128, self.width, self.height),
            self.character_spritesheet.get_sprite(64, 128, self.width, self.height),
            self.character_spritesheet.get_sprite(128, 128, self.width, self.height),
            self.character_spritesheet.get_sprite(192, 128, self.width, self.height),
            self.character_spritesheet.get_sprite(256, 128, self.width, self.height),
            self.character_spritesheet.get_sprite(320, 128, self.width, self.height),
            self.character_spritesheet.get_sprite(384, 128, self.width, self.height),
            self.character_spritesheet.get_sprite(448, 128, self.width, self.height),
            self.character_spritesheet.get_sprite(512, 128, self.width, self.height)
        ]

        self.up_animations = [
            self.character_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(64, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(128, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(192, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(256, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(320, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(384, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(448, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(512, 0, self.width, self.height)
        ]

        self.left_animations = [
            self.character_spritesheet.get_sprite(0, 64, self.width, self.height),
            self.character_spritesheet.get_sprite(64, 64, self.width, self.height),
            self.character_spritesheet.get_sprite(128, 64, self.width, self.height),
            self.character_spritesheet.get_sprite(192, 64, self.width, self.height),
            self.character_spritesheet.get_sprite(256, 64, self.width, self.height),
            self.character_spritesheet.get_sprite(384, 64, self.width, self.height),
            self.character_spritesheet.get_sprite(448, 64, self.width, self.height),
            self.character_spritesheet.get_sprite(512, 64, self.width, self.height)
        ]

        self.right_animations = [
            self.character_spritesheet.get_sprite(0, 192, self.width, self.height),
            self.character_spritesheet.get_sprite(64, 192, self.width, self.height),
            self.character_spritesheet.get_sprite(128, 192, self.width, self.height),
            self.character_spritesheet.get_sprite(192, 192, self.width, self.height),
            self.character_spritesheet.get_sprite(256, 192, self.width, self.height),
            self.character_spritesheet.get_sprite(320, 192, self.width, self.height),
            self.character_spritesheet.get_sprite(384, 192, self.width, self.height),
            self.character_spritesheet.get_sprite(448, 192, self.width, self.height),
            self.character_spritesheet.get_sprite(512, 192, self.width, self.height)
        ]

        self.left_facing_img = self.character_spritesheet.get_sprite(0, 64, self.width, self.height)
        self.right_facing_img = self.character_spritesheet.get_sprite(0, 192, self.width, self.height)
        self.up_facing_img = self.character_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.down_facing_img = self.character_spritesheet.get_sprite(0, 128, self.width, self.height)

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.player_sprite_group, self.game.camera_group)

    def update(self):
        self.movement()
        self.animate()

        self.rect.center += self.direction * PLAYER_SPEED
        # self.collision_rect.x += self.direction * PLAYER_SPEED
        self.collision_rect.center += self.direction * PLAYER_SPEED
        self.collideTerrain('x')
        self.collideTerrain('y')

        if 0 <= self.rect.x <= 400:
            if 0 <= self.rect.y <= 400:
                self.inTown = True
            else:
                self.inTown = False
        else:
            self.inTown = False

        self.x_change = 0
        self.y_change = 0

    def terrainGen(self, direction):
        if len(self.game.terrain_group) < self.MaxTerrain:
            TerrainGenInt = self.MaxTerrain - len(self.game.terrain_group)
            for i in range(TerrainGenInt):
                if direction == 'x':
                    random_x = random.choice((random.randint(self.rect.x - 500, self.rect.x - 400), random.randint(self.rect.x + 400, self.rect.x + 500)))
                    random_y = random.randint(self.rect.y - 400, self.rect.y + 400)
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)
                elif direction == 'y':
                    random_x = random.randint(self.rect.x - 400, self.rect.x + 400)
                    random_y = random.choice((random.randint(self.rect.y - 500, self.rect.y - 400), random.randint(self.rect.y + 400, self.rect.y + 500)))
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)


    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.down_facing_img
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.down_animations) / FPS
                if self.animation_loop >= len(self.down_animations) - 1:
                    self.animation_loop = 0
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.up_facing_img
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.up_animations) / FPS
                if self.animation_loop >= len(self.up_animations) - 1:
                    self.animation_loop = 0
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.left_facing_img
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.left_animations) / FPS
                if self.animation_loop >= len(self.left_animations) - 1:
                    self.animation_loop = 0
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.right_facing_img
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.right_animations) / FPS
                if self.animation_loop >= len(self.right_animations) - 1:
                    self.animation_loop = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change = 1
            self.direction.x = -1
            self.facing = 'left'
            # self.terrainGen('x')
            if len(self.game.terrain_group) < self.MaxTerrain:
                TerrainGenInt = self.MaxTerrain - len(self.game.terrain_group)
                for i in range(TerrainGenInt):
                    random_x = randint(self.rect.x - 425, self.rect.x - 400)
                    random_y = randint(self.rect.y - 425, self.rect.y + 425)
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)

        elif keys[pygame.K_RIGHT]:
            self.x_change = 1
            self.direction.x = 1
            self.facing = 'right'
            # self.terrainGen('x')
            if len(self.game.terrain_group) < self.MaxTerrain:
                TerrainGenInt = self.MaxTerrain - len(self.game.terrain_group)
                for i in range(TerrainGenInt):
                    random_x = randint(self.rect.x + 400, self.rect.x + 425)
                    random_y = random.randint(self.rect.y - 425, self.rect.y + 425)
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)
        else:
            self.direction.x = 0


        if keys[pygame.K_UP]:
            self.y_change  = 1
            self.direction.y = -1
            self.facing = 'up'
            # self.terrainGen('y')
            if len(self.game.terrain_group) < self.MaxTerrain:
                TerrainGenInt = self.MaxTerrain - len(self.game.terrain_group)
                for i in range(TerrainGenInt):
                    random_x = randint(self.rect.x - 425, self.rect.x + 425)
                    random_y = randint(self.rect.y - 425, self.rect.y - 400)
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)
        elif keys[pygame.K_DOWN]:
            self.y_change = 1
            self.direction.y = 1
            self.facing = 'down'
            # self.terrainGen('y')
            if len(self.game.terrain_group) < self.MaxTerrain:
                TerrainGenInt = self.MaxTerrain - len(self.game.terrain_group)
                for i in range(TerrainGenInt):
                    random_x = randint(self.rect.x - 425, self.rect.x + 425)
                    random_y = randint(self.rect.y + 400, self.rect.y + 425)
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)
        else:
            self.direction.y = 0

    def collideTerrain(self, direction):

        if direction == 'x':
            for sprite in self.game.terrain_group:
                collide = pygame.Rect.colliderect(self.collision_rect, sprite.collision_rect)
                if collide:
                    if self.direction.x > 0:  # Moving right
                        self.collision_rect.right = sprite.collision_rect.left
                        self.rect.right = self.collision_rect.right + self.collision_x_offset

                    if self.direction.x < 0:  # Moving Left
                        self.collision_rect.left = sprite.collision_rect.right
                        self.rect.left = sprite.collision_rect.right - self.collision_x_offset

        if direction == 'y':
            for sprite in self.game.terrain_group:
                collide = pygame.Rect.colliderect(self.collision_rect, sprite.collision_rect)
                if collide:
                    if self.direction.y > 0:  # Moving Down
                        self.collision_rect.bottom = sprite.collision_rect.top
                        self.rect.bottom = self.collision_rect.bottom

                    if self.direction.y < 0:  # Moving Up
                        self.collision_rect.top = sprite.collision_rect.bottom
                        self.rect.top = sprite.collision_rect.bottom - self.collision_height_offset


class CharacterSlot1(Character):
    def __init__(self, game, pos):
        Character.__init__(self, game, pos)

        # self.collision_rect = pygame.Rect(pos[0], pos[1], 25, 25)

        self.left_facing_img = self.character_spritesheet.get_sprite(0, 64, self.width, self.height)
        self.right_facing_img = self.character_spritesheet.get_sprite(0, 192, self.width, self.height)
        self.up_facing_img = self.character_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.down_facing_img = self.character_spritesheet.get_sprite(0, 128, self.width, self.height)

        self.down_animations = [self.character_spritesheet.get_sprite(0, 128, self.width, self.height),
                                self.character_spritesheet.get_sprite(64, 128, self.width, self.height),
                                self.character_spritesheet.get_sprite(128, 128, self.width, self.height),
                                self.character_spritesheet.get_sprite(192, 128, self.width, self.height),
                                self.character_spritesheet.get_sprite(256, 128, self.width, self.height),
                                self.character_spritesheet.get_sprite(320, 128, self.width, self.height),
                                self.character_spritesheet.get_sprite(384, 128, self.width, self.height),
                                self.character_spritesheet.get_sprite(448, 128, self.width, self.height),
                                self.character_spritesheet.get_sprite(512, 128, self.width, self.height)
                                ]

        self.up_animations = [self.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.character_spritesheet.get_sprite(64, 0, self.width, self.height),
                              self.character_spritesheet.get_sprite(128, 0, self.width, self.height),
                              self.character_spritesheet.get_sprite(192, 0, self.width, self.height),
                              self.character_spritesheet.get_sprite(256, 0, self.width, self.height),
                              self.character_spritesheet.get_sprite(320, 0, self.width, self.height),
                              self.character_spritesheet.get_sprite(384, 0, self.width, self.height),
                              self.character_spritesheet.get_sprite(448, 0, self.width, self.height),
                              self.character_spritesheet.get_sprite(512, 0, self.width, self.height)
                              ]

        self.left_animations = [self.character_spritesheet.get_sprite(0, 64, self.width, self.height),
                                self.character_spritesheet.get_sprite(64, 64, self.width, self.height),
                                self.character_spritesheet.get_sprite(128, 64, self.width, self.height),
                                self.character_spritesheet.get_sprite(192, 64, self.width, self.height),
                                self.character_spritesheet.get_sprite(256, 64, self.width, self.height),
                                self.character_spritesheet.get_sprite(384, 64, self.width, self.height),
                                self.character_spritesheet.get_sprite(448, 64, self.width, self.height),
                                self.character_spritesheet.get_sprite(512, 64, self.width, self.height)
                                ]

        self.right_animations = [self.character_spritesheet.get_sprite(0, 192, self.width, self.height),
                                 self.character_spritesheet.get_sprite(64, 192, self.width, self.height),
                                 self.character_spritesheet.get_sprite(128, 192, self.width, self.height),
                                 self.character_spritesheet.get_sprite(192, 192, self.width, self.height),
                                 self.character_spritesheet.get_sprite(256, 192, self.width, self.height),
                                 self.character_spritesheet.get_sprite(320, 192, self.width, self.height),
                                 self.character_spritesheet.get_sprite(384, 192, self.width, self.height),
                                 self.character_spritesheet.get_sprite(448, 192, self.width, self.height),
                                 self.character_spritesheet.get_sprite(512, 192, self.width, self.height)
                                 ]
