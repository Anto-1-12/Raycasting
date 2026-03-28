from operator import itemgetter

import pygame
import time
from math import *

class Raycasting_game:

    def __init__(self):

        self.run = True
        self.view_3d = True
        self.pressed_p = False

        self.screen = pygame.display.set_mode((960, 480))
        self.pressed = pygame.key.get_pressed()

        self.map_size = 10
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.block_size = int(self.height / self.map_size)

        self.player_x = -30
        self.player_y = -30
        self.player_orientation = 0

        self.fov = radians(80)
        self.render_distance = 2000

        self.draw_buffer = []

        self.map = \
            [
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
        self.stamp = time.time()
        self.old_stamp = self.stamp

        self.draw_stamp = time.time()
        self.old_draw_stamp = self.draw_stamp

        self.tps_max = 60
        self.fps_max = 120

    def draw_ray(self, ori, size, color):

        ray_x = self.player_x + self.height / 2 - size * cos(ori)
        ray_y = self.player_y + self.height / 2 - size * sin(ori)

        pygame.draw.line(self.screen, color,(self.player_x + self.height / 2, self.player_y + self.height / 2), (ray_x, ray_y))

    def draw_map(self):

        pygame.display.flip()
        self.screen.fill((0, 0, 0))

        for y in range(self.map_size):

            for x in range(self.map_size):

                if self.map[y][x] == 1:
                    pygame.draw.rect(self.screen, (100, 100, 100),(x * self.block_size, y * self.block_size, self.block_size - 1, self.block_size - 1))

                else:
                    pygame.draw.rect(self.screen, (50, 50, 50),(x * self.block_size, y * self.block_size, self.block_size - 1, self.block_size - 1))

        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.player_x + self.height/2), int(self.player_y + self.height/2)), 5)

    def draw_3d(self):

        self.draw_buffer.sort(key=itemgetter(2))

        size_pixel = self.width / degrees(self.fov)

        new_pixel_x = 0

        new_pixel_y_top = 0

        for i in self.draw_buffer:

            if i[0]:

                old_pixel_x = new_pixel_x

                old_pixel_y_top = new_pixel_y_top

                new_pixel_x = degrees(i[2]) * size_pixel
                new_pixel_y_top = i[1]

                #bleu
                pygame.draw.line(self.screen, (0, 0, 255), (new_pixel_x, self.height / 2 + new_pixel_y_top),
                                 (old_pixel_x, self.height / 2 + old_pixel_y_top))
                #rouge
                pygame.draw.line(self.screen, (255, 0, 0), (new_pixel_x, self.height / 2 - new_pixel_y_top),
                                 (old_pixel_x, self.height / 2 - old_pixel_y_top))
                #vert
                pygame.draw.line(self.screen, (0, 255,0), (new_pixel_x, self.height / 2 + new_pixel_y_top),
                                 (new_pixel_x, self.height / 2 - new_pixel_y_top))


        pygame.draw.line(self.screen, (0, 0, 0), (self.width / 2, self.height / 2 - 10),
                         (self.width / 2, self.height / 2 + 10))
        pygame.draw.line(self.screen, (0, 0, 0), (self.width / 2 - 10, self.height / 2),
                         (self.width / 2 + 10, self.height / 2))

        #color = 150 / (1 + ray_size * ray_size * 0.0001) + 100
        #pygame.draw.rect(self.screen, (color, color, color), (((angle_trigo + 0.00001) * size_pixel), (self.height / 2) - (height_wall / 2), size_pixel, height_wall))

    def wall_test(self,x,y):
        if self.map[y][x] == 1:
            return True
        return False

    def for_3d(self,angle,ray_size,is_first_ray):

        reel_ray_size = cos(angle - self.player_orientation) * ray_size

        angle_ver = angle - self.player_orientation + self.fov/2
        if not is_first_ray:
            angle_ver = angle_ver % (pi*2)

        height_wall = (self.height - 10000) / (reel_ray_size + 0.0001)

        self.draw_buffer.append([True, height_wall,angle_ver,reel_ray_size])


    def ray_cast(self):

        if self.view_3d:
            pygame.display.flip()
            self.screen.fill((15, 160, 255))

            self.draw_buffer = []

        else:
            self.draw_ray(self.player_orientation - self.fov / 2 ,100, (255,0,0))
            self.draw_ray(self.player_orientation + self.fov / 2, 100, (255,0,0))
            self.draw_ray(self.player_orientation, 100 ,(255,0,255))

        corner_coo = [[0,0],[self.block_size,0],[0,self.block_size],[self.block_size,self.block_size]]

        for ray in range(2):

            if ray == 0:
                angle = self.player_orientation - self.fov/2
                is_first_ray = True
            else:
                angle = self.player_orientation + self.fov/2
                is_first_ray = False

            for ray_size in range(self.render_distance):

                ray_x = self.player_x + self.height / 2 - ray_size * cos(angle)
                ray_y = self.player_y + self.height / 2 - ray_size * sin(angle)

                block_pos_ray_x = int(ray_x / self.block_size)
                block_pos_ray_y = int(ray_y / self.block_size)

                if self.map[block_pos_ray_y][block_pos_ray_x] == 1:
                    if not self.view_3d:
                        pygame.draw.line(self.screen, (233, 166, 49),(self.player_x + self.height / 2, self.player_y + self.height / 2), (ray_x, ray_y))
                    else:
                        self.for_3d(angle, ray_size,is_first_ray)
                    break

        for y in range(self.map_size):

            for x in range(self.map_size):

                for ray in range(2):

                    if self.wall_test(x,y):

                        nb_boucle = 1

                        try:
                            if not self.wall_test(x,y+1):
                                nb_boucle = 2
                        except:
                            nb_boucle = 2

                        for boucle in range(nb_boucle):

                            dx = x * self.block_size - (self.player_x + self.height / 2)
                            dy = y * self.block_size - (self.player_y + self.height / 2)

                            if nb_boucle > 1:
                                dx += corner_coo[ray + boucle + 1][0]
                                dy += corner_coo[ray + boucle + 1][1]
                            else:
                                dx += corner_coo[ray][0]
                                dy += corner_coo[ray][1]

                            ray_size = sqrt(dx ** 2 + dy ** 2)
                            angle = -atan2( dy, -dx)

                            player_orientation = self.player_orientation % (2 * pi)
                            angle = angle % (2 * pi)

                            fov_start = (player_orientation - self.fov / 2) % (2 * pi)
                            fov_end = (player_orientation + self.fov / 2) % (2 * pi)

                            if fov_start < fov_end:
                                in_fov = fov_start <= angle <= fov_end
                            else:
                                in_fov = angle >= fov_start or angle <= fov_end

                            if ray_size <= self.render_distance and in_fov:

                                step = 10
                                ray_x = self.player_x + self.height / 2
                                ray_y = self.player_y + self.height / 2

                                total_steps = int((ray_size - 10) / step)

                                touch_wall = False

                                for i in range(total_steps):

                                    ray_x -= step * cos(angle)
                                    ray_y -= step * sin(angle)

                                    block_pos_x = int(ray_x // self.block_size)
                                    block_pos_y = int(ray_y // self.block_size)

                                    if self.wall_test(block_pos_x, block_pos_y):
                                        touch_wall = True
                                        break

                                if not touch_wall:
                                    if self.view_3d:
                                        self.for_3d(angle, ray_size, False)

                                    else:
                                        if nb_boucle > 1:
                                            pygame.draw.line(self.screen, (233, 166, 49), (self.player_x + self.height / 2, self.player_y + self.height / 2), ((x * self.block_size) + corner_coo[ray + boucle + 1][0],(y * self.block_size) + corner_coo[ray + boucle + 1][1]))
                                        else:
                                            pygame.draw.line(self.screen, (233, 166, 49),(self.player_x + self.height / 2, self.player_y + self.height / 2),((x * self.block_size)+corner_coo[ray][0], (y * self.block_size)+corner_coo[ray][1]))

        if self.view_3d:
            self.draw_3d()

    def colision_detect(self, plus_ou_moin):

        if plus_ou_moin == "plus":
            block_pos_player_x = int((self.player_x + self.height/2 - (cos(self.player_orientation) * 2.5)) / self.block_size)
            block_pos_player_y = int((self.player_y + self.height/2 - (sin(self.player_orientation) * 2.5)) / self.block_size)

        elif plus_ou_moin == "moin":
            block_pos_player_x = int((self.player_x + self.height/2 + (cos(self.player_orientation) * 2.5)) / self.block_size)
            block_pos_player_y = int((self.player_y + self.height/2 + (sin(self.player_orientation) * 2.5)) / self.block_size)

        if self.map[block_pos_player_y][block_pos_player_x] == 1:
            return False
        else:
            return True

    def inputs(self):

        self.pressed = pygame.key.get_pressed()

        if self.pressed[pygame.K_DELETE]:
            self.run = False

        if self.pressed[pygame.K_LEFT]:
            if self.player_orientation <= radians(0):
                self.player_orientation = radians(360)
            self.player_orientation -= 0.04

        if self.pressed[pygame.K_RIGHT]:
            if self.player_orientation >= radians(360):
                self.player_orientation = 0
            self.player_orientation += 0.04

        if self.pressed[pygame.K_UP] and self.colision_detect("plus"):
            self.player_x -= cos(self.player_orientation) * 2.5
            self.player_y -= sin(self.player_orientation) * 2.5

        if self.pressed[pygame.K_DOWN] and self.colision_detect("moin"):
            self.player_x += cos(self.player_orientation) * 2.5
            self.player_y += sin(self.player_orientation) * 2.5

        if self.pressed[pygame.K_F3]:
            for i in self.draw_buffer:
                print(i[2])
            print("\n")

        if self.pressed[pygame.K_p] and not self.pressed_p:

            if self.view_3d:

                self.view_3d = False
                screen_1 = pygame.display.set_mode((480, 480))
                self.block_size = int(screen_1.get_height() / self.map_size)
                self.height = self.screen.get_height()
                self.width = self.screen.get_width()

            else:

                self.view_3d = True
                screen_1 = pygame.display.set_mode((960, 480))
                self.block_size = int(screen_1.get_height() / self.map_size)
                self.height = self.screen.get_height()
                self.width = self.screen.get_width()

            self.pressed_p = True

        elif not self.pressed[pygame.K_p] and self.pressed_p:
            self.pressed_p = False

        for pygame_event in pygame.event.get():
            if pygame_event.type == pygame.QUIT:
                self.run = False



    def run_game(self):
        time.sleep(1/self.fps_max)
        while self.run:
            if self.stamp - self.old_stamp > 1/self.tps_max:
                self.inputs()
                self.old_stamp = self.stamp
            self.stamp = time.time()

            if self.draw_stamp - self.old_draw_stamp > 1 / self.fps_max:
                if not self.view_3d:
                    self.draw_map()
                self.ray_cast()
                self.old_draw_stamp = self.draw_stamp
            self.draw_stamp = time.time()

pygame.init()
game = Raycasting_game()
game.run_game()
pygame.quit()