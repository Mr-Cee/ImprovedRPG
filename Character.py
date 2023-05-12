import math
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
        self.MaxTerrain = 1

        self.width = 64
        self.height = 64
        self.collision_x_offset = 22
        self.collision_y_offset = 5
        self.collision_width_offset = 22
        self.collision_height_offset = 5

        self.x_change = 0
        self.y_change = 0
        self.direction = pygame.math.Vector2()
        self.movement_loop = 0

        self.facing = 'down'
        self.animation_loop = 1
        self.animation_loop_speed = 0.5

        self.character_spritesheet = SpriteSheet('assets/CharacterWalkingSpritesheet.png')
        self.image = self.character_spritesheet.get_sprite(0, 192, self.width, self.height)
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = pygame.Rect(pos[0] + self.collision_x_offset, pos[1] - self.collision_y_offset, self.width - self.collision_width_offset, self.height - self.collision_height_offset)

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
        self.collision_rect.center = self.rect.center
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
            if len(self.game.terrain_group) < self.MaxTerrain:
                TerrainGenInt = self.MaxTerrain - len(self.game.terrain_group)
                for i in range(TerrainGenInt):
                    random_x = randint(self.rect.x - 500, self.rect.x - 400)
                    random_y = randint(self.rect.y - 500, self.rect.y + 500)
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)
        elif keys[pygame.K_RIGHT]:
            self.x_change = 1
            self.direction.x = 1
            self.facing = 'right'
            if len(self.game.terrain_group) < self.MaxTerrain:
                TerrainGenInt = self.MaxTerrain - len(self.game.terrain_group)
                for i in range(TerrainGenInt):
                    random_x = randint(self.rect.x + 400, self.rect.x + 500)
                    random_y = randint(self.rect.y - 500, self.rect.y + 500)
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)
        else:
            self.direction.x = 0


        if keys[pygame.K_UP]:
            self.y_change  = 1
            self.direction.y = -1
            self.facing = 'up'
            if len(self.game.terrain_group) < self.MaxTerrain:
                TerrainGenInt = self.MaxTerrain - len(self.game.terrain_group)
                for i in range(TerrainGenInt):
                    random_x = randint(self.rect.x - 500, self.rect.x + 500)
                    random_y = randint(self.rect.y - 500, self.rect.y - 400)
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)
        elif keys[pygame.K_DOWN]:
            self.y_change = 1
            self.direction.y = 1
            self.facing = 'down'
            if len(self.game.terrain_group) < self.MaxTerrain:
                TerrainGenInt = self.MaxTerrain - len(self.game.terrain_group)
                for i in range(TerrainGenInt):
                    random_x = randint(self.rect.x - 500, self.rect.x + 500)
                    random_y = randint(self.rect.y + 400, self.rect.y + 500)
                    Tree(self.game, (random_x, random_y), self.game.terrain_group)
        else:
            self.direction.y = 0

    def collideTerrain(self, direction):
        for sprite in self.game.terrain_group:
            collide = pygame.Rect.colliderect(self.collision_rect, sprite.collision_rect)
            if direction == 'x':
                if collide:
                    if self.direction.x > 0:  # Moving right
                        self.rect.right = sprite.collision_rect.left + self.collision_x_offset
                        self.collision_rect.right = sprite.collision_rect.left
                    if self.direction.x < 0:  # Moving Left
                        self.rect.left = sprite.collision_rect.right - self.collision_width_offset
                        self.collision_rect.left = sprite.collision_rect.right
            if direction == 'y':
                if collide:
                    if self.direction.y > 0:  # Moving Down
                        self.rect.bottom = sprite.collision_rect.top
                        self.collision_rect.bottom = sprite.collision_rect.top
                        print('------------------------------------------------')
                        print('Player:'+str(self.rect.bottom), str(self.collision_rect.bottom))
                        print('Object:'+str(sprite.collision_rect.top))
                        print('-----------------------------------------------')
                    if self.direction.y < 0:  # Moving Up
                        self.rect.top = sprite.collision_rect.bottom - self.height + self.collision_height_offset
                        self.collision_rect.top = sprite.collision_rect.bottom

class CharacterSlot1(Character):
    def __init__(self, game, pos):
        Character.__init__(self, game, pos)

        self.collision_rect = pygame.Rect(pos[0], pos[1], 25, 25)

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
