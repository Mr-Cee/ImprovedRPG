import sys
from random import randint

import pygame

from CameraGroup import CameraGroup
from Character import *
from Terrain import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.camera_group = CameraGroup()
        self.player_sprite_group = pygame.sprite.Group()
        self.terrain_group = pygame.sprite.Group()
        self.CollisionBool = True

        self.inTownText = self.font.render('In Town', True, BLACK)
        self.inTownTextRect = self.inTownText.get_rect()
        self.inTownTextRect.center = (WIN_WIDTH - 50, 25)
        self.MainTownCoord = (500, 500)
        self.MainTownRect = pygame.Rect(self.MainTownCoord[0], self.MainTownCoord[1], 400, 400)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.CollisionBool = not self.CollisionBool

    def new(self):
        self.playing = True
        self.player = CharacterSlot1(self, (WIN_WIDTH / 2, WIN_HEIGHT / 2))

        for i in range(20):
            random_x = randint(0, WIN_WIDTH)
            random_y = randint(0, WIN_HEIGHT)
            # random_x = 475
            # random_y = 475
            Tree(self, (random_x, random_y), self.terrain_group)

    def update(self):
        self.all_sprites.update()
        self.terrain_group.update()
        self.camera_group.update()

        # if 100 <= self.player.rect.x <= 500:
        #     if 100 <= self.player.rect.y <= 500:
        #         self.player.inTown = True
        #
        #     else:
        #         self.player.inTown = False
        # else:
        #     self.player.inTown = False


        # if len(self.terrain_group) < 20:
        #     TerrainGenInt = 20 - len(self.terrain_group)
        #     for i in range(TerrainGenInt):
        #         random_x = randint(self.player.rect.x-500, self.player.rect.x+500)
        #         random_y = randint(self.player.rect.y-500, self.player.rect.y+500)
        #         Tree(self, (random_x, random_y), self.terrain_group)

    def draw(self):
        self.camera_group.custom_draw(self, self.player)
        if self.player.inTown:
            self.screen.blit(self.inTownText, self.inTownTextRect)
        self.clock.tick(FPS)



        # for object in self.terrain_group:
        #     pygame.draw.rect(self.screen, BLACK, object.collision_rect)
        # for sprite in self.player_sprite_group:
        #     pygame.draw.rect(self.screen, WHITE, sprite.collision_rect)


        pygame.display.update()

    def intro_screen(self):
        pass

    def game_over_screen(self):
        pass

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()


g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over_screen()

pygame.quit()
sys.exit()
