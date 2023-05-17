import pygame

# Game Window Settings
WIN_WIDTH = 800
WIN_HEIGHT = 800
GAME_WIDTH = WIN_WIDTH
GAME_HEIGHT = WIN_HEIGHT
FPS = 60



# Color Keys
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Images
BACKGROUND_IMG = pygame.image.load('assets/LargeBackground.png')

# Timers
EnemyMovementTimer = pygame.USEREVENT + 1

# Player Settings
PLAYER_SPEED = 2
ENEMY_SPEED = 1

# Town Settings
TownListDictionary = {} # {Town: ID}
TownDistanceDictionary = {} # {Distance: ID}

# Terrain Settings
TerrainGenEdgeW = WIN_HEIGHT/2 + 100
TerrainGenEdgeH = WIN_HEIGHT/2 + 100


