from operator import itemgetter

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
def draw_lign(deppart,arrivee):
    distance = sqrt((arrivee[0] - deppart[0]) ** 2 + (arrivee[1] - deppart[1]) ** 2)
    angle = cos((arrivee[0] - deppart[0])/distance)
    ray_size = 0
    for i in range(int(distance)):

        ray_x = deppart[0] - ray_size * cos(angle)
        ray_y = deppart[1] - ray_size * sin(angle)

        casioplot.set_pixel(ray_x, ray_y, (0, 0, 0))
        ray_size += 1


def draw_3d(draw_buffer):
    width = 384
    height = 192
    draw_buffer.sort(key=itemgetter(2))

    size_pixel = width / degrees(fov)

    new_pixel_x = 0

    new_pixel_y_top = 0

    for i in draw_buffer:

        if i[0]:
            old_pixel_x = new_pixel_x

            old_pixel_y_top = new_pixel_y_top

            new_pixel_x = degrees(i[2]) * size_pixel
            new_pixel_y_top = i[1]

            # bleu

            draw_lign((new_pixel_x,height / 2 + new_pixel_y_top),(old_pixel_x, height / 2 + old_pixel_y_top))
            # rouge

            draw_lign((new_pixel_x, height / 2 - new_pixel_y_top), (old_pixel_x, height / 2 - old_pixel_y_top))
            # vert

            draw_lign((new_pixel_x, height / 2 + new_pixel_y_top), (old_pixel_x, height / 2 - old_pixel_y_top))


def for_3d(angle,ray_size,is_first_ray):
    height = 192

    reel_ray_size = cos(angle - player_orientation) * ray_size

    angle_ver = angle - player_orientation + fov/2
    if not is_first_ray:
        angle_ver = angle_ver % (pi*2)

    height_wall = (height - 10000) / (reel_ray_size + 0.0001)

    return [True, height_wall,angle_ver,reel_ray_size]

def wall_test(x, y, map2):
    if map2[y][x] == 1:
        return True
    return False



def ray_cast():

    casioplot.clear_screen()
    height = 192

    draw_buffer = []

    corner_coo = [[0, 0], [block_size_x, 0], [0,block_size_y], [block_size_x, block_size_y]]

    for ray in range(2):

        if ray == 0:
            angle = player_orientation - fov / 2
            is_first_ray = True
        else:
            angle = player_orientation + fov / 2
            is_first_ray = False

        for ray_size in range(render_distance):

            ray_x = player_x + height / 2 - ray_size * cos(angle)
            ray_y = player_y + height / 2 - ray_size * sin(angle)

            block_pos_ray_x = int(ray_x / block_size_x)
            block_pos_ray_y = int(ray_y / block_size_y)

            try:
                if wall_test(block_pos_ray_x,block_pos_ray_y,map):
                    for_3d(angle, ray_size, is_first_ray)
                    break
            except:
                pass

    for y in range(map_size):

        for x in range(map_size):

            for ray in range(2):

                if wall_test(x, y,map):

                    nb_boucle = 1

                    try:
                        if not wall_test(x, y + 1,map):
                            nb_boucle = 2
                    except:
                        nb_boucle = 2

                    for boucle in range(nb_boucle):

                        dx = x * block_size_x - (player_x + height / 2)
                        dy = y * block_size_y - (player_y + height / 2)

                        if nb_boucle > 1:
                            dx += corner_coo[ray + boucle + 1][0]
                            dy += corner_coo[ray + boucle + 1][1]
                        else:
                            dx += corner_coo[ray][0]
                            dy += corner_coo[ray][1]

                        ray_size = sqrt(dx ** 2 + dy ** 2)
                        angle = -atan2(dy, -dx)

                        player_orientation2 = player_orientation % (2 * pi)
                        angle = angle % (2 * pi)

                        fov_start = (player_orientation2 - fov / 2) % (2 * pi)
                        fov_end = (player_orientation2 + fov / 2) % (2 * pi)

                        if fov_start < fov_end:
                            in_fov = fov_start <= angle <= fov_end
                        else:
                            in_fov = angle >= fov_start or angle <= fov_end

                        if ray_size <= render_distance and in_fov:

                            step = 10
                            ray_x = player_x + height / 2
                            ray_y = player_y + height / 2

                            total_steps = int((ray_size - 10) / step)

                            touch_wall = False

                            for i in range(total_steps):

                                ray_x -= step * cos(angle)
                                ray_y -= step * sin(angle)

                                block_pos_x = int(ray_x // block_size_x)
                                block_pos_y = int(ray_y // block_size_y)

                                if wall_test(block_pos_x, block_pos_y,map):
                                    touch_wall = True
                                    break

                            if not touch_wall:
                                draw_buffer.append(for_3d(angle, ray_size, False))

    draw_3d(draw_buffer)


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