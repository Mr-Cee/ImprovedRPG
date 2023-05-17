import sys
from random import randint

import pygame

from CameraGroup import CameraGroup
from Character import *
from Terrain import *
from Town import *
from Enemy import *


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
        self.enemy_group = pygame.sprite.Group()
        self.CollisionBool = True

        self.inTownText = self.font.render('In Town', True, BLACK)
        self.inTownTextRect = self.inTownText.get_rect()
        self.inTownTextRect.topright = (WIN_WIDTH - 50, 25)
        self.MainTown = MainTown((500, 500), "Main", 0)
        self.TownList = [self.MainTown]
        TownListDictionary[self.MainTown.ID] = self.MainTown
        TownDistanceDictionary[self.MainTown.ID] = self.MainTown.distanceToPlayer

        self.MainTownCoord = (500, 500)
        self.MainTownRect = pygame.Rect(self.MainTownCoord[0], self.MainTownCoord[1], 400, 400)

    def generateTerrain(self):
        for sprite in self.terrain_group:
            sprite.kill()

        for i in range(20):
            random_terrain = random.choice(Terrain.TerrainTemplate.TerrainList)
            random_x = randint(0, WIN_WIDTH)
            random_y = randint(0, WIN_HEIGHT)
            if random_terrain == 'Tree':
                Tree(self, (random_x, random_y), self.terrain_group)
            elif random_terrain == 'Rock':
                Rock(self, (random_x, random_y), self.terrain_group)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.CollisionBool = not self.CollisionBool
                if event.key == pygame.K_t:
                    if not self.player.inTown:
                        self.TP_pos = self.player.rect.center
                        print('Teleporting to closest town: ' + TownListDictionary[
                            min(TownDistanceDictionary, key=TownDistanceDictionary.get)].name)
                        self.player.rect.center = TownListDictionary[
                            min(TownDistanceDictionary, key=TownDistanceDictionary.get)].rect.center
                        self.player.collision_rect = pygame.Rect(self.player.rect.left + self.player.collision_x_offset,
                                                                 self.player.rect.top + self.player.collision_y_offset,
                                                                 self.player.width - self.player.collision_width_offset,
                                                                 self.player.height - self.player.collision_height_offset)
                        self.generateTerrain()
                    else:
                        print("Going back to previous Location")
                        self.player.rect.center = self.TP_pos
                        self.player.collision_rect = pygame.Rect(self.player.rect.left + self.player.collision_x_offset,
                                                                 self.player.rect.top + self.player.collision_y_offset,
                                                                 self.player.width - self.player.collision_width_offset,
                                                                 self.player.height - self.player.collision_height_offset)
                        current_pos = None
                        self.generateTerrain()

                    self.generateTerrain()
                if event.key == pygame.K_s:
                    EnemyTemplate(self, (self.player.rect.centerx, self.player.rect.centery+100),10, 10, 10 )



    def new(self):
        self.playing = True
        self.player = CharacterSlot1(self, (WIN_WIDTH / 2, WIN_HEIGHT / 2))

        for i in range(20):
            random_x = randint(0, WIN_WIDTH)
            random_y = randint(0, WIN_HEIGHT)
            Tree(self, (random_x, random_y), self.terrain_group)
        Wolf = EnemyTemplate(self, (400, 600), 10, 10, 10)


    def update(self):
        self.all_sprites.update()
        self.camera_group.update()


    def draw(self):
        self.camera_group.custom_draw(self, self.player)
        if self.player.inTown:
            self.screen.blit(self.inTownText, self.inTownTextRect)
        self.clock.tick(FPS)

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
