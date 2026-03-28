try:
    from gint import*
    gint = True
except:
    gint = False

try:
    import keyboard
    keyboard_can = True

except:
    keyboard_can = False

import casioplot
from math import *

casioplot.show_screen()

map_size = 7
block_size_x = int(192 / map_size)
block_size_y = int(384 / map_size)

player_x = 192 / 2
player_y = 384 / 2
player_orientation = 0

fov = 96
render_distance = 1000
nb_ray = fov
ray_angle_incrementation = 0.6

run = True

map = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0 ,1],
    [1, 0, 0, 0, 0, 0 ,1],
    [1, 0, 0, 0, 0, 0 ,1],
    [1, 0, 0, 0, 0, 0 ,1],
    [1, 0, 0, 0, 0, 0 ,1],
    [1, 1, 1, 1, 1, 1, 1]
]

def draw_3d(ray_size, angle):

    size_pixel = 384 / nb_ray

    height_wall_bottom = int(71 + 4300/(ray_size+0.0001))

    height_wall_top = int(71 - 4300/(ray_size+0.0001))

    casioplot.set_pixel(int((angle+0.00001)*size_pixel), height_wall_top , (0,0,0))

    casioplot.set_pixel(int((angle+0.00001)*size_pixel), height_wall_bottom, (0, 0, 0))

def ray_cast():

    casioplot.clear_screen()

    angle_depart = -radians(player_orientation) + radians(fov/2)

    for angle in range(nb_ray,-1,-1):

        ray_size = 0
        render = True

        while ray_size != render_distance and render == True:

            ray_x = player_x - ray_size * cos(angle_depart)
            ray_y = player_y + ray_size * sin(angle_depart)

            block_pos_ray_x = int(ray_x/block_size_x)
            block_pos_ray_y = int(ray_y/block_size_y)

            if map[block_pos_ray_x][block_pos_ray_y] == 1:

                draw_3d(ray_size,angle)
                render = False

            ray_size += 1


        angle_depart += radians(ray_angle_incrementation)

def colision_detect(plus_ou_moin):

    if plus_ou_moin == "plus":
        block_pos_player_x = int(player_x + (-sin(radians(player_orientation))) / block_size_x)
        block_pos_player_y = int(player_y + (cos(radians(player_orientation))) / block_size_y)

    elif plus_ou_moin == "moin":
        block_pos_player_x = int(player_x - -sin(radians(player_orientation)))
        block_pos_player_y = int(player_y - cos(radians(player_orientation)))

    if map[int(block_pos_player_x/block_size_x)][int(block_pos_player_y/block_size_y)] == 1:
        return False
    else:
        return True

while run:

    if keyboard_can:

        if keyboard.is_pressed('esc'):
            run = False

        if keyboard.is_pressed('left'):
            player_orientation -= 3

        elif keyboard.is_pressed('right'):
            player_orientation += 3

        elif keyboard.is_pressed('up') and colision_detect("plus"):
            player_x += -sin(radians(player_orientation))
            player_y += cos(radians(player_orientation))

        elif keyboard.is_pressed('down') and colision_detect("moin"):
            player_x -= -sin(radians(player_orientation))
            player_y -= cos(radians(player_orientation))

    if gint:

        e = pollevent()

        if e.type == KEYEV_DOWN and e.key in [KEY_7]:
            run = False

        if e.type == KEYEV_DOWN and e.key in [KEY_1]:
            player_orientation -= 3

        elif e.type == KEYEV_DOWN and e.key in [KEY_3]:
            player_orientation += 3

        elif e.type == KEYEV_DOWN and e.key in [KEY_5] and colision_detect("plus"):
            player_x += -sin(radians(player_orientation))
            player_y += cos(radians(player_orientation))

        elif e.type == KEYEV_DOWN and e.key in [KEY_2] and colision_detect("moin"):
            player_x -= -sin(radians(player_orientation))
            player_y -= cos(radians(player_orientation))

    casioplot.show_screen()
    ray_cast()