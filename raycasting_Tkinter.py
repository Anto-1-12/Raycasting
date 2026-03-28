from tkinter import *
import tkinter as tk
from math import *
import keyboard

class app:

    def __init__(self):

        self.app = tk.Tk()
        self.app.title("Raycasting")
        self.app.config(bg="gray30")
        self.app.geometry("400x600")
        self.Canvas_draw_pixel = Canvas(self.app, width=400, height=600, bg='ivory')
        self.Canvas_draw_pixel.place(x=0,y=0)

        self.map_button = Button(self.app , text = "M" , width = 2 , height= 1 ,relief = GROOVE , bg="white" , font=('broadway', 18),command = self.draw_3d_or_not)
        self.map_button.pack()
        self.map_button.place(x=350,y=3)

        self.up_button = Button(self.app, text="^\n|", width=2, height=1, relief=GROOVE, bg="white",font=('broadway', 18), command=self.go_up)
        self.up_button.pack()
        self.up_button.place(x=50, y=500)

        self.down_button = Button(self.app, text="|\nv", width=2, height=1, relief=GROOVE, bg="white",font=('broadway', 18), command=self.go_down)
        self.down_button.pack()
        self.down_button.place(x=50, y=550)

        self.left_button = Button(self.app, text="<-", width=2, height=1, relief=GROOVE, bg="white",font=('broadway', 18), command=self.ori_left)
        self.left_button.pack()
        self.left_button.place(x=5, y=550)

        self.right_button = Button(self.app, text="->", width=2, height=1, relief=GROOVE, bg="white",font=('broadway', 18), command=self.ori_right)
        self.right_button.pack()
        self.right_button.place(x=95, y=550)

        self.map_button = Button(self.app, text="X", width=2, height=1, relief=GROOVE, bg="white",font=('broadway', 18), command=self.do_run_false)
        self.map_button.pack()
        self.map_button.place(x=3, y=3)

        self.height = 600
        self.width = 400

        self.map_size = 10
        self.block_size_x = int(self.width / self.map_size)
        self.block_size_y = int(self.height / self.map_size)

        self.player_x = self.width / 2 - 30
        self.player_y = self.height / 2 - 30
        self.player_orientation = 0

        self.fov = 96
        self.render_distance = 1000
        self.nb_ray = self.fov
        self.ray_angle_incrementation = 0.6

        self.run = True
        self.pressed_p = False
        self.view_3d = True

        self.map = [
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

        self.Canvas_draw_pixel.create_rectangle(0, 0, self.width, self.height, fill="white", activefill="white", outline="white")

        for x in range(self.map_size):

            for y in range(self.map_size):

                if self.map[x][y] == 1:
                    self.Canvas_draw_pixel.create_rectangle(x * self.block_size_x, y * self.block_size_y,
                                                            (x+1) * self.block_size_x, (y+1) * self.block_size_y,
                                                            fill="snow3")
                    #pygame.draw.rect(screen_1, (100, 100, 100),(x * block_size_x, y * block_size_y, block_size_y - 1, block_size_x - 1))

                else:
                    self.Canvas_draw_pixel.create_rectangle(x * self.block_size_x, y * self.block_size_y,
                                                            (x + 1) * self.block_size_x, (y + 1) * self.block_size_y,
                                                            fill="snow4")
                    #pygame.draw.rect(screen_1, (50, 50, 50),(x * block_size_x, y * block_size_y, block_size_y - 1, block_size_x - 1))

            self.Canvas_draw_pixel.create_oval(self.player_x-2,self.player_y-2,self.player_x+2,self.player_y+2,fill="red",outline="red")
            #pygame.draw.circle(screen_1, (255, 0, 0), (int(player_x), int(player_y)), 5)

    def draw_3d(self,ray_size, angle):

        size_pixel = 400 /self.nb_ray

        height_wall_bottom = int(self.height/2 + 4300 / (ray_size + 0.0001))

        height_wall_top = int(self.height/2 - 4300 / (ray_size + 0.0001))

        self.Canvas_draw_pixel.create_rectangle(int(angle), height_wall_bottom, int((angle+0.00001)*size_pixel), height_wall_top, fill="black")



    def ray_cast(self):

        if self.view_3d:

            self.Canvas_draw_pixel.create_rectangle(0, 0, self.width, self.height, fill="white")

        angle_depart = -radians(self.player_orientation) + radians(self.fov/2)

        for angle in range(self.nb_ray,-1,-1):

            ray_size = 0
            render = True

            while ray_size != self.render_distance and render == True:

                ray_x = self.player_x - ray_size * cos(angle_depart)
                ray_y = self.player_y + ray_size * sin(angle_depart)

                block_pos_ray_x = int(ray_x/self.block_size_x)
                block_pos_ray_y = int(ray_y/self.block_size_y)

                if self.map[block_pos_ray_x][block_pos_ray_y] == 1:
                    if self.view_3d:
                        self.draw_3d(ray_size,angle)
                    else:
                        self.Canvas_draw_pixel.create_line(self.player_x, self.player_y, ray_x, ray_y, fill="orange")
                        #pygame.draw.line(screen_1, (233, 166, 49), (player_x, player_y), (ray_x, ray_y))

                    render = False

                ray_size += 1


            angle_depart += radians(self.ray_angle_incrementation)

    def colision_detect(self,plus_ou_moin):

        if plus_ou_moin == "plus":
            block_pos_player_x = int(self.player_x + (-sin(radians(self.player_orientation))) / self.block_size_x)
            block_pos_player_y = int(self.player_y + (cos(radians(self.player_orientation))) / self.block_size_y)

        elif plus_ou_moin == "moin":
            block_pos_player_x = int(self.player_x - -sin(radians(self.player_orientation)))
            block_pos_player_y = int(self.player_y - cos(radians(self.player_orientation)))

        if self.map[int(block_pos_player_x/self.block_size_x)][int(block_pos_player_y/self.block_size_y)] == 1:
            return False
        else:
            return True

    def draw_3d_or_not(self):
        if self.view_3d:
            self.view_3d = False

        else:
            self.view_3d = True

    def go_up(self):

        if self.colision_detect("plus"):
                self.player_x += -sin(radians(self.player_orientation))
                self.player_y += cos(radians(self.player_orientation))

    def go_down(self):
        if self.colision_detect("moin"):
                self.player_x -= -sin(radians(self.player_orientation))
                self.player_y -= cos(radians(self.player_orientation))

    def ori_left(self):
        self.player_orientation -= 3

    def ori_right(self):
        self.player_orientation += 3

    def mainloop(self):

        while self.run:

            if keyboard.is_pressed('esc'):
                self.run = False

            if keyboard.is_pressed('left'):
                self.ori_left()

            elif keyboard.is_pressed('right'):
                self.ori_right()

            elif keyboard.is_pressed('up'):
                self.go_up()

            elif keyboard.is_pressed('down'):
                self.go_down()

            if keyboard.is_pressed('p') and not self.pressed_p:
                self.draw_3d_or_not()
                self.pressed_p = True

            elif not keyboard.is_pressed('p') and self.pressed_p:
                self.pressed_p = False

            if not self.view_3d:
                self.draw_map()
            self.ray_cast()
            self.app.update()

    def tkinter_event(self):
        self.mainloop()

    def do_run_false(self):
        self.run = False

app = app()
app.tkinter_event()