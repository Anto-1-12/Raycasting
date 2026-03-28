import pygame
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
        self.render_distance = 1000
        self.nb_ray = 30
        self.ray_angle_incrementation = self.fov / self.nb_ray

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

    def draw_3d(self, ray_size, angle,angle_depart):

        size_pixel = self.width / self.nb_ray

        if angle_depart > self.player_orientation:
            reel_ray_size = cos(angle_depart - self.player_orientation) * ray_size

        elif angle_depart < self.player_orientation:
            reel_ray_size = cos(self.player_orientation - angle_depart) * ray_size

        elif angle_depart == self.player_orientation:
            reel_ray_size = ray_size

        color = 150 / (1 + ray_size * ray_size * 0.0001) + 100

        height_wall_bottom = self.height + 100 / (reel_ray_size + 0.0001)

        height_wall_top = self.height - 100 / (reel_ray_size + 0.0001)

        height_wall = (height_wall_bottom - height_wall_top) * 50

        pygame.draw.rect(self.screen, (color, color, color), (((angle + 0.00001) * size_pixel), (self.height / 2) - (height_wall / 2), size_pixel, height_wall))

    def ray_cast(self):

        if self.view_3d:
            pygame.display.flip()
            self.screen.fill((15, 160, 255))

        angle_depart = self.player_orientation - self.fov / 2

        for angle in range(self.nb_ray):

            ray_size = 0
            render = True

            while ray_size != self.render_distance and render == True:

                ray_x = self.player_x + self.height / 2 - ray_size * cos(angle_depart)
                ray_y = self.player_y + self.height / 2 - ray_size * sin(angle_depart)

                block_pos_ray_x = int(ray_x / self.block_size)
                block_pos_ray_y = int(ray_y / self.block_size)

                if self.map[block_pos_ray_y][block_pos_ray_x] == 1:

                    render = False
                    if self.view_3d:
                        self.draw_3d(ray_size, angle, angle_depart)
                        pygame.draw.line(self.screen, (0, 0, 0),(self.width / 2, self.height / 2 - 10),(self.width / 2, self.height / 2 + 10))

                        pygame.draw.line(self.screen, (0, 0, 0),(self.width / 2 - 10, self.height / 2),(self.width / 2 + 10, self.height / 2))
                    else:
                        pygame.draw.line(self.screen, (233, 166, 49), (self.player_x + self.height / 2, self.player_y + self.height / 2), (ray_x, ray_y))

                ray_size += 0.4

            angle_depart += self.ray_angle_incrementation

    def colision_detect(self, plus_ou_moin):

        if plus_ou_moin == "plus":
            block_pos_player_x = int((self.player_x + self.height/2 - (cos(self.player_orientation) * 0.5)) / self.block_size)
            block_pos_player_y = int((self.player_y + self.height/2 - (sin(self.player_orientation) * 0.5)) / self.block_size)

        elif plus_ou_moin == "moin":
            block_pos_player_x = int((self.player_x + self.height/2 + (cos(self.player_orientation) * 0.5)) / self.block_size)
            block_pos_player_y = int((self.player_y + self.height/2 + (sin(self.player_orientation) * 0.5)) / self.block_size)

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
            self.player_orientation -= 0.005

        if self.pressed[pygame.K_RIGHT]:
            if self.player_orientation >= radians(360):
                self.player_orientation = 0
            self.player_orientation += 0.005

        if self.pressed[pygame.K_UP] and self.colision_detect("plus"):
            self.player_x -= cos(self.player_orientation) * 0.5
            self.player_y -= sin(self.player_orientation) * 0.5

        if self.pressed[pygame.K_DOWN] and self.colision_detect("moin"):
            self.player_x += cos(self.player_orientation) * 0.5
            self.player_y += sin(self.player_orientation) * 0.5

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

        while self.run:

            self.inputs()

            if not self.view_3d:
                self.draw_map()

            self.ray_cast()

pygame.init()
game = Raycasting_game()
game.run_game()
pygame.quit()