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
        self.direction = math.atan2(self.y-(random.randint(self.y-self.max_travel, self.y + self.max_travel)),
                                    self.x - (random.randint(self.x-self.max_travel, self.x+self.max_travel)))
        self.direction2 = 0.125
        print(self.direction2)
        self.speed_x = -1
        self.speed_y = 0
        self.collisionCount = 0

        self.inCombat = False

        self.image = SpriteSheet('assets/Wolfsheet1.png').get_sprite(0, 0, 32, 64)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.right_animations = []
        self.up_animations = []
        self.left_animations = []
        self.attack_animations = []
        self.death_animations = []

    def update(self):
        self.collideTerrain()
        self.movement()
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


    def movementDirectionChange(self):
        self.direction2 *= -1
        self.speed_x = random.randint(0, 8) * self.direction2
        self.speed_y = random.randint(0, 8) * self.direction2
        if self.speed_x == 0 and self.speed_y == 0:
            self.speed_x = random.randint(1, 8) * self.direction2
            self.speed_y = random.randint(1, 8) * self.direction2

    def movement(self):
        if self.canMove:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.movementDirectionChange()
                self.canMove = False
                self.movement_loop = 0
                self.movementDelay = pygame.time.get_ticks() + self.movementPause

    def animate(self):
        pass

    def collideTerrain(self):
        for sprite in self.game.terrain_group:
            collide = pygame.Rect.colliderect(self.rect, sprite.rect)
            if collide:
                self.movementDirectionChange()
        for sprite in self.game.TownList:
            collide = pygame.Rect.colliderect(self.rect, sprite.rect)
            if collide:
                self.movementDirectionChange()

