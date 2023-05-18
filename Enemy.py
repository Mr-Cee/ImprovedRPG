import math
import random

import pygame

from SpriteUtilities import SpriteSheet
from CONFIG import *


class EnemyTemplate(pygame.sprite.Sprite):
    def __init__(self, game, pos, AttackStrength, Health, EXPWorth):
        self.game = game
        self.x, self.y = pos
        self.AttackPower = AttackStrength
        self.max_hp = Health
        self.hp = self.max_hp
        self.exp = EXPWorth
        self.enemyName = 'ChangeMe'


        super().__init__(self.game.all_sprites, self.game.enemy_group, self.game.camera_group)

        self.width = 64
        self.height = 64

        self.x_change = 0
        self.y_change = 0
        self.direction = pygame.math.Vector2()
        self.facing = 'left'
        self.facing_list = ['left', 'right', 'up', 'down']
        self.animation_loop = 0
        self.movement_loop = 0
        self.movementDelay = 0
        self.movementPause = 2000
        self.max_travel = 100
        self.canMove = True
        self.dt = ENEMY_SPEED
        self.direction2 = (1/30)
        self.speed_x = random.randint(-30,30)*self.direction2
        self.speed_y = random.randint(-30,30)*self.direction2
        self.collisionCount = 0

        self.inCombat = False

        self.image = SpriteSheet('assets/Wolfsheet1.png').get_sprite(0, 0, 32, 64)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.right_animations = []
        self.up_animations = []
        self.down_animations = []
        self.left_animations = []
        self.attack_animations = []
        self.death_animations = []
        self.deathAnimation = False

    def update(self):

        self.movement()
        self.collideTerrain()
        self.animate()


        time_now = pygame.time.get_ticks()
        if time_now < self.movementDelay:
            self.canMove = False
        else:
            self.canMove = True

        if not (self.game.player.rect.centerx-TerrainGenEdgeW) < self.rect.centerx < (self.game.player.rect.centerx+TerrainGenEdgeW):
            self.kill()
        if not (self.game.player.rect.centery - TerrainGenEdgeH) < self.rect.centery < (
                self.game.player.rect.centery + TerrainGenEdgeH):
            self.kill()

    def getFacing(self):
        if abs(self.speed_x) > abs(self.speed_y):
            if self.speed_x > 0:
                self.facing = 'right'
            else:
                self.facing = 'left'
            self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, 64, 32)
        else:
            if self.speed_y > 0:
                self.facing = 'down'
            else:
                self.facing = 'up'
            self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, 32, 64)

    def movementDirectionChange(self):
        self.direction2 *= -1
        self.speed_x = round(random.randint(-30, 30) * self.direction2,2)
        self.speed_y = round(random.randint(-30, 30) * self.direction2,2)
        if self.speed_x == 0 and self.speed_y == 0:
            self.speed_x = round(random.randint(-30, 30) * self.direction2,2)
            self.speed_y = round(random.randint(-30, 30) * self.direction2,2)

        self.getFacing()
        print('facing: ' + self.facing + '...' + str(self.speed_x)+','+str(self.speed_y))

    def movement(self):
        if self.canMove:
            self.rect.x += self.speed_x
            self.collision_rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collision_rect.y += self.speed_y
            if self.facing == 'up':
                self.y_change = -1
                self.x_change = 0
            elif self.facing == 'down':
                self.y_change = 1
                self.x_change = 0
            elif self.facing == 'right':
                self.y_change = 0
                self.x_change = 1
            elif self.facing == 'left':
                self.y_change = 0
                self.x_change = -1

            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.movementDirectionChange()
                self.canMove = False
                self.x_change = 0
                self.y_change = 0
                self.movement_loop = 0
                self.movementPause = random.randint(2000, 7000)
                self.movementDelay = pygame.time.get_ticks() + self.movementPause

    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.down_animations)/FPS
                if self.animation_loop >= len(self.down_animations) - 1:
                    self.animation_loop = 0
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.up_animations)/FPS
                if self.animation_loop >= len(self.up_animations) - 1:
                    self.animation_loop = 0
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.left_animations)/FPS
                if self.animation_loop >= len(self.left_animations) - 1:
                    self.animation_loop = 0
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.right_animations)/FPS
                if self.animation_loop >= len(self.right_animations) - 1:
                    self.animation_loop = 0
        if self.deathAnimation:
            self.image = self.death_animations[math.floor(self.animation_loop)]
            self.animation_loop += len(self.death_animations) / (FPS*2)
            if self.animation_loop >= len(self.death_animations) - 1:
                self.animation_loop = 0
                self.kill()

    def collideTerrain(self):
        for sprite in self.game.terrain_group:
            collide = pygame.Rect.colliderect(self.collision_rect, sprite.collision_rect)
            if collide:
                self.movementDirectionChange()
        for sprite in self.game.TownList:
            collide = pygame.Rect.colliderect(self.rect, sprite.rect)
            if collide:
                self.canMove = False
                self.deathAnimation = True
                # self.movementDirectionChange()


class Wolf(EnemyTemplate):
    def __init__(self, game, pos, AttackStrength, Health, EXPWorth):
        super().__init__(game, pos, AttackStrength, Health, EXPWorth)

        self.enemyName = 'a Wolf'

        self.width = 32
        self.height = 64

        self.wolf_spritesheet = SpriteSheet('assets/Wolfsheet1.png')

        self.image = self.wolf_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.down_animations = [self.wolf_spritesheet.get_sprite(0, 128, self.width, self.height),
                                self.wolf_spritesheet.get_sprite(32, 128, self.width, self.height),
                                self.wolf_spritesheet.get_sprite(64, 128, self.width, self.height),
                                self.wolf_spritesheet.get_sprite(96, 128, self.width, self.height)]

        self.up_animations = [self.wolf_spritesheet.get_sprite(160, 132, self.width, self.height),
                              self.wolf_spritesheet.get_sprite(192, 132, self.width, self.height),
                              self.wolf_spritesheet.get_sprite(224, 132, self.width, self.height),
                              self.wolf_spritesheet.get_sprite(256, 132, self.width, self.height)]

        self.left_animations = [self.wolf_spritesheet.get_sprite(320, 288, 64, 32),
                                self.wolf_spritesheet.get_sprite(384, 288, 64, 32),
                                self.wolf_spritesheet.get_sprite(448, 288, 64, 32),
                                self.wolf_spritesheet.get_sprite(512, 288, 64, 32),
                                self.wolf_spritesheet.get_sprite(576, 288, 64, 32)]

        self.right_animations = [self.wolf_spritesheet.get_sprite(320, 96, 64, 32),
                                 self.wolf_spritesheet.get_sprite(384, 96, 64, 32),
                                 self.wolf_spritesheet.get_sprite(448, 96, 64, 32),
                                 self.wolf_spritesheet.get_sprite(512, 96, 64, 32),
                                 self.wolf_spritesheet.get_sprite(576, 96, 64, 32)]

        self.left_attack_animations = [self.wolf_spritesheet.get_sprite(320, 352, 64, 32),
                                       self.wolf_spritesheet.get_sprite(384, 352, 64, 32),
                                       self.wolf_spritesheet.get_sprite(448, 352, 64, 32),
                                       self.wolf_spritesheet.get_sprite(512, 352, 64, 32),
                                       self.wolf_spritesheet.get_sprite(576, 352, 64, 32)]

        self.death_animations = [self.wolf_spritesheet.get_sprite(320, 192, 64, 32),
                                 self.wolf_spritesheet.get_sprite(384, 192, 64, 32),
                                 self.wolf_spritesheet.get_sprite(448, 192, 64, 32),
                                 self.wolf_spritesheet.get_sprite(512, 192, 64, 32)
                                 ]

