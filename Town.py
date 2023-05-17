import pygame


class TownTemplate:
    def __init__(self, pos, name, ID):
        self.pos = pos
        self.name = name
        self.ID = ID
        self.rect = pygame.Rect(pos[0], pos[1], 500, 500)
        self.distanceToPlayer = 0


class MainTown(TownTemplate):
    def __init__(self, pos, name, ID):
        super().__init__(pos, name, ID)


class RandomTown(TownTemplate):
    def __init__(self, pos, name, ID):
        super().__init__(pos, name, ID)
