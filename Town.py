import pygame


class TownTemplate:
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name
        self.rect = pygame.Rect(pos[0], pos[1], 500, 500)
        self.distanceToPlayer = 0


class MainTown(TownTemplate):
    def __init__(self, pos, name):
        super().__init__(pos, name)


class RandomTown(TownTemplate):
    def __init__(self, pos, name):
        super().__init__(pos, name)
