from operator import itemgetter
from math import *
import pygame
import time

class rect:

    def __init__(self,x,y):
        #creation d'un rectangle de largeur la et de longueur lo
        self.x_t = x
        self.y_t = y
        self.nb_geo = 4

    def get_geo(self,coo,cote):
        #renvoie la geo de chaque cote du rect

        if cote == 0:
            # en haut
            return [[coo[0]-(1/2)*self.x_t,coo[1]-(1/2)*self.y_t],[coo[0]+(1/2)*self.x_t,coo[1]-(1/2)*self.y_t]]
        elif cote == 1:
            # a gauche
            return [[coo[0]-(1/2)*self.x_t,coo[1]-(1/2)*self.y_t],[coo[0]-(1/2)*self.x_t,coo[1]+(1/2)*self.y_t]]
        elif cote == 2:
            # en bas
            return [[coo[0]-(1/2)*self.x_t,coo[1]+(1/2)*self.y_t],[coo[0]+(1/2)*self.x_t,coo[1]+(1/2)*self.y_t]]
        elif cote == 3:
            # a droite
            return [[coo[0]+(1/2)*self.x_t,coo[1]-(1/2)*self.y_t],[coo[0]+(1/2)*self.x_t,coo[1]+(1/2)*self.y_t]]

    def get_nb_geo(self):
        return self.nb_geo

    def get_size(self):
        return [self.x_t,self.y_t]

    def test_colision(self, is_entity,coo_extern,coo_intern):
        if not is_entity:
            if (coo_intern[0] - (1/2)*self.x_t < coo_extern[0] < coo_intern[0] + (1/2)*self.x_t) and (coo_intern[1] - (1/2)*self.y_t < coo_extern[1] < coo_intern[1] + (1/2)*self.y_t):
                return True
            else:
                return False

        return False

class block:

    def __init__(self,x,y,h):

        self.geo = rect(50,50)
        self.x = x
        self.y = y
        self.height = h

    def get_coo(self):
        return [self.x, self.y]

    def get_geo(self):
        return self.geo

    def get_height(self):
        return self.height

class wall:

    def __init__(self,x,y,h):

        self.geo = rect(200,50)
        self.x = x
        self.y = y
        self.height = h

    def get_coo(self):
        return [self.x, self.y]

    def get_geo(self):
        return self.geo

    def get_height(self):
        return self.height

class player:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.ori = 0

    def get_ori(self):
        return self.ori

    def get_coo(self):
        return [self.x, self.y]

    def set_coo(self,coo):
        self.x = coo[0]
        self.y = coo[1]

    def set_ori(self,ori):
        self.ori = ori

class raycast:

    def __init__(self, fov, height):

        """
        self.map = [
            block(25,25,25),block(75,25,25),block(125,25,25),block(175,25,25),block(225,25,25),block(275,25,25),block(325,25,25),block(375,25,25),block(425,25,25),block(475,25,25),
            block(25,75,25),block(225, 75, 25),block(475, 75, 25),
            block(25, 125, 25), block(125, 125, 25),block(325, 125, 25),block(475, 125, 25),
            block(25, 175, 25), block(125, 175, 25),block(175, 175, 25),block(225, 175, 25),block(275, 175, 25),block(325, 175, 25),block(375, 175, 25),block(425, 175, 25),block(475, 175, 25),
            block(25, 225, 25), block(125, 225, 25),block(475, 225, 25),
            block(25, 275, 25), block(125, 275, 25),block(225, 275, 25),block(275, 275, 25),block(325, 275, 25),block(375, 275, 25),block(475, 275, 25),
            block(25, 325, 25), block(125, 325, 25),block(225, 325, 25),block(375, 325, 25),block(475, 325, 25),
            block(25, 375, 25), block(125, 375, 25),block(225, 375, 25),block(325, 375, 25),block(375, 375, 25),block(475, 375, 25),
            block(25, 425, 25),block(225, 425, 25),block(475, 425, 25),
            block(25,475,25),block(75,475,25),block(125,475,25),block(175,475,25),block(225,475,25),block(275,475,25),block(325,475,25),block(375,475,25),block(425,475,25),block(475,475,25)
                    ]
        """
        self.map = [block(100,0,25)]
        self.entity = [player(0, 0)]
        self.fov = fov
        self.render_distance = 100000
        self.step = 10
        self.draw_buffer = []
        self.height = height

    def get_draw_buffer(self):
        return self.draw_buffer

    def get_map(self):
        return self.map

    def get_entity(self):
        return self.entity

    def get_player_coo(self):
        return self.entity[0].get_coo()

    def set_player_coo(self,coo):
        self.entity[0].set_coo(coo)

    def get_player_ori(self):
        return self.entity[0].get_ori()

    def set_player_ori(self,ori):
        self.entity[0].set_ori(ori)

    def for_3d(self,angle,ray_size,geo,hauteur):

        reel_ray_size = [cos(angle[0] - self.entity[0].get_ori()) * ray_size[0], cos(angle[1] - self.entity[0].get_ori()) * ray_size[1]]

        rel_angle = [(angle[0] - self.entity[0].get_ori() + pi) % (2 * pi) - pi,(angle[1] - self.entity[0].get_ori() + pi) % (2 * pi) - pi]

        proj_factor = self.height * hauteur

        height_wall = [proj_factor / (reel_ray_size[0] + 0.0001),proj_factor / (reel_ray_size[1] + 0.0001)]

        self.draw_buffer.append([ (ray_size[0] + ray_size[1]) /2 , geo, height_wall,rel_angle])

    def raycast(self,colision_detect):

        self.draw_buffer = []

        fov_start = (self.entity[0].get_ori() - self.fov / 2) % (2 * pi)
        fov_end = (self.entity[0].get_ori() + self.fov / 2) % (2 * pi)
        player_coo = self.entity[0].get_coo()

        #on parcour tout les elements de la map
        for objet in self.map:
            #tout les element pour l'instant ont 4 faces
            for cote in range(objet.get_geo().get_nb_geo()):

                #si la geo est dans le champs de vision (pas just le point mais bien toute la geo de la face selec)
                geo_is_in_fov = False

                #on recupère la geo de la face cote de l'objet selectionné
                geo = objet.get_geo().get_geo(objet.get_coo(),cote)

                angle_buff = []
                ray_buff = []

                #on parcour les deux point qui compose la geo
                for point in geo:
                    #determiner la distance entre le point et le joueur ainsi que l'angle que fait le rayon
                    dx = point[0] - player_coo[0]
                    dy = point[1] - player_coo[1]
                    ray_size = sqrt(dx ** 2 + dy ** 2)
                    angle = atan2( dy, dx)
                    angle = angle % (2 * pi)

                    #stocker les var des des buff
                    angle_buff.append(angle)
                    ray_buff.append(ray_size)

                    #on verifie si la geo est dans le champ de vision
                    if not geo_is_in_fov:
                        if fov_start < fov_end:
                            geo_is_in_fov = fov_start <= angle <= fov_end
                        else:
                            geo_is_in_fov = angle >= fov_start or angle <= fov_end

                if geo_is_in_fov:

                    face_visible = False
                    blocked_by_self = False

                    if colision_detect:
                        for ele in range(len(geo)):
                            #si le rayon est pas trop loin et qu'il est dans la fov

                            if ray_buff[ele] <= self.render_distance:
                                ray_x = player_coo[0]
                                ray_y = player_coo[1]

                                total_steps = int(ray_buff[ele] / self.step)
                                blocked = False

                                for i in range(total_steps):

                                    ray_x += self.step * cos(angle_buff[ele])
                                    ray_y += self.step * sin(angle_buff[ele])

                                    for elements in self.map:
                                        if elements.get_geo().test_colision(False,(ray_x,ray_y),elements.get_coo()):
                                            blocked = True
                                            if elements == objet:
                                                blocked_by_self = True
                                            break
                                    #si mure touché
                                    if blocked or blocked_by_self:
                                        break

                                #si ca na pas touche de mure
                                if not blocked and not blocked_by_self:
                                    #meme si le mure etait considere comme invisible il devient visible car il y a au moin un bout de visible
                                    face_visible = True
                                    break
                    else:
                        face_visible = True

                    if face_visible:
                        self.for_3d(angle_buff, ray_buff, geo,objet.get_height())

class game:

    def __init__(self):

        self.run = True
        self.pressed_p = False
        self.pressed_f3 = False
        self.pressed_i = False
        self.view_3d = True
        self.debug = False
        self.colision_detect = False

        self.screen = pygame.display.set_mode((960, 480))
        self.pressed = pygame.key.get_pressed()
        self.fov = radians(80)

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.ray_engine = raycast(self.fov,self.height)
        self.draw_buffer = []

        self.stamp = time.time()
        self.old_stamp = self.stamp

        self.draw_stamp = time.time()
        self.old_draw_stamp = self.draw_stamp

        self.tps_max = 60
        self.fps_max = 120

    def draw_3d(self):

        self.screen.fill((15, 160, 255))

        for geo in self.draw_buffer:

            distance_du_centre = [(tan(geo[3][0])/tan(self.fov/2))*(self.width/2)+self.width/2,(tan(geo[3][1])/tan(self.fov/2))*(self.width/2)+self.width/2]

            if self.debug:

                #bleu

                pygame.draw.line(self.screen, (0, 0, 255), (distance_du_centre[0], self.height / 2 + geo[2][0]),(distance_du_centre[1], self.height / 2 + geo[2][1]))

                #rouge

                pygame.draw.line(self.screen, (255, 0, 0), (distance_du_centre[0], self.height / 2 - geo[2][0]),(distance_du_centre[1], self.height / 2 - geo[2][1]))

                #vert

                pygame.draw.line(self.screen, (0, 255,0), (distance_du_centre[0], self.height / 2 + geo[2][0]),(distance_du_centre[0], self.height / 2 - geo[2][0]))

                pygame.draw.line(self.screen, (0, 255, 0), (distance_du_centre[1], self.height / 2 + geo[2][1]),(distance_du_centre[1], self.height / 2 - geo[2][1]))

            else:

                pygame.draw.polygon(
                    self.screen,
                    (150, 75, 0),
                    [
                        (distance_du_centre[0], self.height / 2 - geo[2][0]),
                        (distance_du_centre[1], self.height / 2 - geo[2][1]),
                        (distance_du_centre[1], self.height / 2 + geo[2][1]),
                        (distance_du_centre[0], self.height / 2 + geo[2][0])
                    ]
                )

        pygame.draw.line(self.screen, (0, 0, 0), (self.width / 2, self.height / 2 - 10),
                         (self.width / 2, self.height / 2 + 10))
        pygame.draw.line(self.screen, (0, 0, 0), (self.width / 2 - 10, self.height / 2),
                         (self.width / 2 + 10, self.height / 2))

        pygame.display.flip()

        #color = 150 / (1 + ray_size * ray_size * 0.0001) + 100
        #pygame.draw.rect(self.screen, (color, color, color), (((angle_trigo + 0.00001) * size_pixel), (self.height / 2) - (height_wall / 2), size_pixel, height_wall))

    def draw_ray(self, ori, size, color):

        ray_x = self.ray_engine.get_player_coo()[0] + size * cos(ori)
        ray_y = self.ray_engine.get_player_coo()[1] + size * sin(ori)

        pygame.draw.line(self.screen, color,(self.ray_engine.get_player_coo()[0], self.ray_engine.get_player_coo()[1]), (ray_x, ray_y))

    def draw_map(self):

        pygame.display.flip()
        self.screen.fill((0, 0, 0))

        for element in self.ray_engine.get_map():
            pygame.draw.rect(self.screen, (100, 100, 100),(element.get_geo().get_geo(element.get_coo(),0)[0][0], element.get_geo().get_geo(element.get_coo(),0)[0][1], element.get_geo().get_size()[0],element.get_geo().get_size()[1]))

        for ray in self.draw_buffer:
            for geo in ray[1]:
                pygame.draw.line(self.screen, (255,255,255),(self.ray_engine.get_player_coo()[0], self.ray_engine.get_player_coo()[1]), (geo[0], geo[1]))

        self.draw_ray(self.ray_engine.get_player_ori() - self.fov / 2, 100, (255, 0, 0))
        self.draw_ray(self.ray_engine.get_player_ori() + self.fov / 2, 100, (255, 0, 0))
        self.draw_ray(self.ray_engine.get_player_ori(), 100, (255, 0, 255))

        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.ray_engine.get_entity()[0].get_coo()[0]), int(self.ray_engine.get_entity()[0].get_coo()[1])), 5)

    def inputs(self):

        self.pressed = pygame.key.get_pressed()

        if self.pressed[pygame.K_DELETE]:
            self.run = False

        if self.pressed[pygame.K_LEFT]:
            if self.ray_engine.get_player_ori() <= radians(0):
                self.ray_engine.set_player_ori(radians(360))
            self.ray_engine.set_player_ori(self.ray_engine.get_player_ori() - 0.04)

        if self.pressed[pygame.K_RIGHT]:
            if self.ray_engine.get_player_ori() >= radians(360):
                self.ray_engine.set_player_ori(0)
            self.ray_engine.set_player_ori(self.ray_engine.get_player_ori() + 0.04)

        if self.pressed[pygame.K_UP]:
            self.ray_engine.set_player_coo([self.ray_engine.get_player_coo()[0] + cos(self.ray_engine.get_player_ori()) * 2.5,self.ray_engine.get_player_coo()[1] + sin(self.ray_engine.get_player_ori()) * 2.5])

        if self.pressed[pygame.K_DOWN]:
            self.ray_engine.set_player_coo([self.ray_engine.get_player_coo()[0] - cos(self.ray_engine.get_player_ori()) * 2.5, self.ray_engine.get_player_coo()[1] - sin(self.ray_engine.get_player_ori()) * 2.5])

        if self.pressed[pygame.K_p] and not self.pressed_p:

            if self.view_3d:

                self.view_3d = False
                self.screen = pygame.display.set_mode((500, 500))
                self.height = self.screen.get_height()
                self.width = self.screen.get_width()

            else:

                self.view_3d = True
                self.screen = pygame.display.set_mode((960, 480))
                self.height = self.screen.get_height()
                self.width = self.screen.get_width()

            self.pressed_p = True

        elif not self.pressed[pygame.K_p] and self.pressed_p:
            self.pressed_p = False

        if self.pressed[pygame.K_F3] and not self.pressed_f3:

            if self.debug:

                self.debug = False

            else:

                self.debug = True

            self.pressed_f3 = True

        elif not self.pressed[pygame.K_F3] and self.pressed_f3:
            self.pressed_f3 = False

        if self.pressed[pygame.K_i] and not self.pressed_i:

            if self.colision_detect:

                self.colision_detect = False

            else:

                self.colision_detect = True

            self.pressed_i = True

        elif not self.pressed[pygame.K_i] and self.pressed_i:
            self.pressed_i = False

        for pygame_event in pygame.event.get():
            if pygame_event.type == pygame.QUIT:
                self.run = False

    def run_game(self):
            time.sleep(1 / self.fps_max)
            while self.run:
                if self.stamp - self.old_stamp > 1 / self.tps_max:
                    self.inputs()
                    self.old_stamp = self.stamp
                self.stamp = time.time()

                if self.draw_stamp - self.old_draw_stamp > 1 / self.fps_max:
                    self.ray_engine.raycast(self.colision_detect)
                    self.draw_buffer = self.ray_engine.get_draw_buffer()
                    self.draw_buffer.sort(key=itemgetter(0))
                    if not self.view_3d:
                        self.draw_map()
                    else:
                        self.draw_3d()
                        pass
                    self.old_draw_stamp = self.draw_stamp
                self.draw_stamp = time.time()

pygame.init()
game = game()
game.run_game()
pygame.quit()