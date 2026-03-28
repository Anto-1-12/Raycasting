######################################
#
#    Simple raycasting with PyGame
#
#                 by
#
#          Code Monkey King
#
######################################

# packages
import pygame
import sys
import math

# global constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = int((SCREEN_WIDTH/2) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 20
STEP_ANGLE = FOV / CASTED_RAYS

# global variables
player_x = (SCREEN_WIDTH/2) / 2
player_y = (SCREEN_WIDTH/2) / 2
player_angle = math.pi

# map
MAP = (
    '########'
    '# #    #'
    '# #  ###'
    '#      #'
    '#      #'
    '#  ##  #'
    '#   #  #'
    '########'
)

# init pygame
pygame.init()

# create game window
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set window title
pygame.display.set_caption('Raycasting')

# init timer
clock = pygame.time.Clock()
def draw_map():
# colors
    light_grey = (191, 191, 191)
    dark_grey = (65, 65, 65)

# iterate over map
    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
        # calculate square index
            square = i * MAP_SIZE + j

        # draw map
            pygame.draw.rect(win,
                            light_grey if MAP[square] == '#' else dark_grey,
                            (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
# raycasting algorithm
def cast_rays():
    # define left most angle of FOV
    start_angle = player_angle - HALF_FOV

    # loop over casted rays
    for ray in range(CASTED_RAYS):
        # cast ray step by step
        for depth in range(MAX_DEPTH):
            # get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # covert target X, Y coordinate to map col, row
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            # calculate map square index
            square = row * MAP_SIZE + col

            # ray hits the condition
            if MAP[square] == '#':
                break

            SCALE = (SCREEN_WIDTH) / CASTED_RAYS

            # wall shading
            color = 255 / (1 + depth * depth * 0.0001)

            # calculate wall height
            wall_height = 21000 / (depth + 0.0001)
            # draw 3D projection
            pygame.draw.rect(win, (color, color, color),(ray * SCALE,(SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))

        # increment angle by a single step
        start_angle += STEP_ANGLE


# game loop
while True:
    # escape condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    # update background
    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (100, 100, 100), (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 200, 200), (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    # apply raycasting
    cast_rays()
    draw_map()

    # get user input
    keys = pygame.key.get_pressed()

    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)

    # calculate map square index
    square = row * MAP_SIZE + col

    # player hits the wall (collision detection)
    if MAP[square] == '#':

        can_go_up = False

    else:
        can_go_up = True

    # handle user input
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]and can_go_up:
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5

    # update display
    pygame.display.flip()

    # set FPS
    clock.tick(30)
