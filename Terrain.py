import pygame.sprite


class TerrainTemplate(pygame.sprite.Sprite):
    def __init__(self, game, pos, group):
        self.game = game
        super().__init__(self.game.all_sprites, self.game.camera_group, group)
        self.image = pygame.image.load('assets/tree.png')  # Defaults to Tree Image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        if not (self.game.player.rect.x-425) <= self.rect.x <= (self.game.player.rect.x+425):
            self.kill()
        elif not (self.game.player.rect.y-425) <= self.rect.y <= (self.game.player.rect.y+425):
            self.kill()

        # print(self.rect)



class Tree(TerrainTemplate):
    def __init__(self, game, pos, group):
        super().__init__(game, pos, group)
        self.image = pygame.image.load('assets/tree.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect(pos[0]+25, pos[1]+35, self.image.get_width()-50, self.image.get_height()-45)

