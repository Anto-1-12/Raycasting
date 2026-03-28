import pygame
from math import *

pygame.init()

screen_1 = pygame.display.set_mode((960, 480))
screen_1.fill((255, 255, 255))
pygame.display.set_caption("Raycasting")
clock = pygame.time.Clock()
map_size = 10
block_size_x = int(screen_1.get_height() / map_size)
block_size_y = int(screen_1.get_width() / map_size)

player_x = screen_1.get_height() / 2 - 30
player_y = screen_1.get_width() / 2 - 30
player_orientation = pi

fov = radians(80)
render_distance = 1000
nb_ray = 120
ray_angle_incrementation = fov/nb_ray

run = True
pressed_p = False
view_3d = True

map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0 ,0 ,0 ,0 ,1],
    [1, 0, 1, 0, 0, 0 ,1 ,0 ,0 ,1],
    [1, 0, 1, 1, 1, 1 ,1 ,1 ,1 ,1],
    [1, 0, 1, 0, 0, 0 ,0 ,0 ,0 ,1],
    [1, 0, 1, 0, 1, 1 ,1 ,1 ,0 ,1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def draw_map():
    pygame.display.flip()
    screen_1.fill((0, 0, 0))

    for y in range(map_size):

        for x in range(map_size):

            if map[y][x] == 1:
                pygame.draw.rect(screen_1, (100, 100, 100),(x * block_size_x, y * block_size_y, block_size_y - 1, block_size_x - 1))

            else:
                pygame.draw.rect(screen_1, (50, 50, 50),(x * block_size_x, y * block_size_y, block_size_y - 1, block_size_x - 1))

        pygame.draw.circle(screen_1, (255, 0, 0), (int(player_x), int(player_y)), 5)

def draw_3d(ray_size, angle,ori):

    size_pixel = screen_1.get_width() / nb_ray

    reel_ray_size = ray_size

    color = 150 / (1 + ray_size * ray_size * 0.0001) + 100

    height_wall_bottom = int(screen_1.get_height() + 4300 / (reel_ray_size + 0.0001))

    height_wall_top = int(screen_1.get_height() - 4300 / (reel_ray_size + 0.0001))

    height_wall = height_wall_bottom - height_wall_top

    pygame.draw.rect(screen_1,(color,color,color),(((angle+0.00001)*size_pixel),(screen_1.get_height() /2)-(height_wall / 2),size_pixel,height_wall))

def ray_cast():

    if view_3d:
        pygame.display.flip()
        screen_1.fill((15, 160, 255))

    angle_depart = player_orientation + fov/2

    for angle in range(nb_ray):

        ray_size = 0
        render = True

        while ray_size != render_distance and render == True:

            ray_x = player_x - ray_size * cos(-angle_depart)
            ray_y = player_y - ray_size * sin(-angle_depart)

            block_pos_ray_x = int(ray_x/block_size_x)
            block_pos_ray_y = int(ray_y/block_size_y)

            if map[block_pos_ray_y][block_pos_ray_x] == 1:
                render = False
                if view_3d:
                    draw_3d(ray_size,angle,angle_depart)
                    pygame.draw.line(screen_1, (0, 0, 0), (screen_1.get_width() / 2, screen_1.get_height() / 2 - 10), (screen_1.get_width() / 2, screen_1.get_height() / 2 + 10))
                    pygame.draw.line(screen_1, (0, 0, 0), (screen_1.get_width() / 2 - 10, screen_1.get_height() / 2),(screen_1.get_width() / 2 + 10, screen_1.get_height() / 2))
                else:
                    pygame.draw.line(screen_1, (233, 166, 49), (player_x, player_y), (ray_x, ray_y))

            ray_size += 1


        angle_depart -= ray_angle_incrementation

def colision_detect(plus_ou_moin):

    if plus_ou_moin == "plus":
        block_pos_player_x = int((player_x - cos(player_orientation)) / block_size_x)
        block_pos_player_y = int((player_y - sin(player_orientation)) / block_size_y)

    elif plus_ou_moin == "moin":
        block_pos_player_x = int((player_x + cos(player_orientation)) / block_size_x)
        block_pos_player_y = int((player_y + sin(player_orientation)) / block_size_y)

    if map[block_pos_player_y][block_pos_player_x] == 1:
        return False
    else:
        return True

while run:

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_DELETE]:
        run = False

    if pressed[pygame.K_LEFT]:
        player_orientation += 0.05

    if pressed[pygame.K_RIGHT]:
        player_orientation -= 0.05

    if pressed[pygame.K_UP] and colision_detect("plus"):
        player_x -= cos(player_orientation)
        player_y -= sin(player_orientation)

    if pressed[pygame.K_DOWN] and colision_detect("moin"):
        player_x += cos(player_orientation)
        player_y += sin(player_orientation)

    if pressed[pygame.K_p] and not pressed_p:
        if view_3d:
            view_3d = False
            screen_1 = pygame.display.set_mode((480, 480))
            block_size_x = int(screen_1.get_height() / map_size)
            block_size_y = int(screen_1.get_width() / map_size)

            player_y = (player_y / 960) * 480
        else:
            view_3d = True
            screen_1 = pygame.display.set_mode((960, 480))
            block_size_x = int(screen_1.get_height() / map_size)
            block_size_y = int(screen_1.get_width() / map_size)

            player_y = (player_y / 480) * 960
        pressed_p = True

    elif not pressed[pygame.K_p] and pressed_p:
        pressed_p = False

    for pygame_event in pygame.event.get():
        if pygame_event.type == pygame.QUIT:
            run = False

    if not view_3d:
        draw_map()
    ray_cast()