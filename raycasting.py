from math import *

import pygame



class Game:

    def __init__(self):
        self.render_distance = 10
        self.x_ray = 0
        self.y_ray = 0
        self.x_player = 0
        self.y_player = 0
        self.ray_size = 0.1
        self.player_orientation = 0
        self.ray_orientation = 0
        self.fov = 100
        self.pixel_gris = []
        self.oppose = 0

        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Raycasting")
        self.clock = pygame.time.Clock()

        self.run = True

        self.coo_mur = [
            [1,1,1,1,1,1],
            [1,0,0,0,0,1],
            [1,0,0,0,0,1],
            [1,0,0,0,0,1],
            [1,0,0,0,0,1],
            [1,1,1,1,1,1]
        ]

    def add_pixel(self):
    
        self.ray_size += 0.1
    
        self.oppose = tan(radians(self.ray_orientation)) * self.ray_size
        self.x_ray = self.oppose
        self.y_ray = self.ray_size
    
    def distance(self):
        return self.ray_size / cos(radians(self.ray_orientation))
    
    def ray_cast(self):

        self.x_ray = self.x_player
        self.y_ray = self.y_player
        self.ray_size = self.y_ray

        self.ray_orientation = self.player_orientation + (self.fov / 2)

        for z in range(self.fov):
    
            self.ray_size = 0

            for i in range(self.render_distance):
    
                loop_count = 0
    
                for a in self.coo_mur:
        
                    loop_count_2 = 0
        
                    for t in a:
            
                        if self.x_ray < loop_count + 1 and self.x_ray >= loop_count and self.y_ray < loop_count_2 + 1 and self.y_ray >= loop_count_2 and t == 1:
                
                            self.pixel_gris.append([self.x_ray,self.y_ray, self.distance()])
                
                        loop_count_2 += 1
            
                        self.add_pixel()
            
                    loop_count += 1

            self.ray_orientation -= 1

    def print_ray(self):

        pygame.display.flip()
        self.screen.fill((255, 255, 255))

        loop_count = 0

        for i in self.pixel_gris:

            for a in range(28):
                pygame.draw.line(self.screen,(0,0,0), (loop_count+a,(720/2)-i[2]*20),(loop_count+a,(720/2)+i[2]*20))
            loop_count += 28

    def key_event(self):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_DELETE]:
            self.run = False

        if pressed[pygame.K_LEFT]:
            self.player_orientation += 1

        if pressed[pygame.K_RIGHT]:
            self.player_orientation -= 1

        if pressed[pygame.K_UP]:
            self.x_player += 1

        if pressed[pygame.K_DOWN]:
            self.x_player -= 1

        for pygame_event in pygame.event.get():
            if pygame_event.type == pygame.QUIT:
                self.run = False

    def debug(self):

        print("player orientation :",self.player_orientation)
        print("x player :",self.x_player)
        print("y player :",self.y_player)
        try:
            print("pixel gris :",self.pixel_gris)
        except:
            print("pas de pixel_gris")

    def event(self):

        while self.run:

            self.ray_cast()
            self.print_ray()
            self.key_event()
            self.clock.tick(60)
            self.debug()

            if not self.run:
                print(self.pixel_gris)
                quit()

            self.pixel_gris = []

game = Game()
game.event()