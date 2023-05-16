import pygame
from CONFIG import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera Offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Ground
        self.ground_surf = pygame.image.load('assets/LargeBackground.png').convert()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))
        self.ground_width = self.ground_surf.get_width()
        self.ground_height = self.ground_surf.get_height()

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, game, player):
        self.game = game
        self.center_target_camera(player)

        # Ground
        ground_offset = self.ground_rect.topleft - self.offset
        # self.display_surface.blit(self.ground_surf, (0, 0))
        self.display_surface.fill(BLACK)
        self.display_surface.blit(self.ground_surf, ground_offset)

        # Draw Main Town line
        for town in self.game.TownList:
            pygame.draw.rect(self.display_surface, BLACK, (town.rect[0] - self.offset[0], town.rect[1]-self.offset[1], town.rect[2], town.rect[3]), 2)

        # Active Elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        if self.game.player.inTown:
            self.display_surface.blit(self.game.inTownText, self.game.inTownTextRect)


        #
        # for object in self.game.terrain_group:
        #     pygame.draw.rect(self.display_surface, BLACK, (object.collision_rect[0]-self.offset[0], object.collision_rect[1] - self.offset[1], object.collision_rect[2], object.collision_rect[3]))
        # for sprite in self.game.player_sprite_group:
        #     if self.game.CollisionBool:
        #         pygame.draw.rect(self.display_surface, WHITE, (sprite.collision_rect[0]-self.offset[0], sprite.collision_rect[1] - self.offset[1], sprite.collision_rect[2], sprite.collision_rect[3]))
        #     else:
        #         pygame.draw.rect(self.display_surface, WHITE, (sprite.rect[0]-self.offset[0], sprite.rect[1] - self.offset[1], sprite.rect[2], sprite.rect[3]))


        # pygame.display.update()
            # self.display_surface.blit(sprite.image, sprite.rect)
