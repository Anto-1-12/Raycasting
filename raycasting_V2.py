from math import *

import pygame


class Game:

    def __init__(self):
        self.x_ray = 0
        self.y_ray = 0
        self.player_orientation = 0
        self.ray_orientation = pi
        self.casted_ray = 30

        pygame.init()
        self.screen = pygame.display.set_mode((960, 480))
        pygame.display.set_caption("Raycasting")
        self.clock = pygame.time.Clock()

        self.hauteur_ecran = self.screen.get_height()

        self.map_size = 10

        self.x_player = (self.screen.get_width()/2)/2
        self.y_player = (self.screen.get_width()/2)/2

        self.tile_size = int((self.screen.get_width()/2) / self.map_size)
        self.render_distance = self.map_size * self.tile_size

        self.fov = pi / 3
        self.half_fov = self.fov / 2
        self.step_angle = self.fov / self.casted_ray

        self.run = True

        self.map = ('1111111111'
                    '1000000001'
                    '1000010001'
                    '1000010001'
                    '1000010001'
                    '1000000001'
                    '1010010001'
                    '1010000001'
                    '1010000001'
                    '1111111111')

        self.wall_coo = [
            1,1,1,1,1,1,1,1,1,1,
            1,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,1,0,0,0,1,
            1,0,0,0,0,1,0,0,0,1,
            1,0,0,0,0,1,0,0,0,1,
            1,0,0,0,0,0,0,0,0,1,
            1,0,1,0,0,1,0,0,0,1,
            1,0,1,0,0,0,0,0,0,1,
            1,0,1,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,1,1
        ]
    
    def ray_cast(self):

        start_angle = self.player_orientation - self.half_fov

        # loop over casted rays
        for ray in range(self.casted_ray):
            # cast ray step by step
            for depth in range(self.render_distance):

                target_x = self.x_player - sin(start_angle) * depth
                target_y = self.y_player + cos(start_angle) * depth

                # covert target X, Y coordinate to map col, row
                col = int(target_x / self.tile_size)
                row = int(target_y / self.tile_size)

                # calculate map square index
                square = row * self.map_size + col

                # ray hits the condition
                if self.wall_coo[square] == 1:
                    break

                scale = (self.screen.get_width()) / self.casted_ray

                # wall shading
                color = 255 / (1 + depth * depth * 0.0001)

                # calculate wall height
                wall_height = 30000 / (depth + 0.0001)

                pygame.draw.rect(self.screen, (color, color, color),(ray * scale,(self.screen.get_height() / 2) - wall_height / 2, scale, wall_height))



            # increment angle by a single step
            start_angle += self.step_angle

    def key_event(self):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_DELETE]:
            self.run = False

        if pressed[pygame.K_LEFT]:
            self.player_orientation -= 0.05

        if pressed[pygame.K_RIGHT]:
            self.player_orientation += 0.05

        if pressed[pygame.K_UP]:
            self.x_player += -sin(self.player_orientation) * 5
            self.y_player += cos(self.player_orientation) * 5

        if pressed[pygame.K_DOWN]:
            self.x_player -= -sin(self.player_orientation) * 5
            self.y_player -= cos(self.player_orientation) * 5

        for pygame_event in pygame.event.get():
            if pygame_event.type == pygame.QUIT:
                self.run = False

    def event(self):

        while self.run:

            pygame.display.flip()
            self.ray_cast()
            self.key_event()
            self.clock.tick(120)

            if not self.run:
                quit()

game = Game()
game.event()