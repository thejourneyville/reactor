import pygame
import random

# initializing pygame
pygame.init()

# screen/surface setup:
phone_w, phone_h = 500, 500
display_info_object = pygame.display.Info()
screen_width, screen_height = display_info_object.current_w, display_info_object.current_h
screen_scaler = phone_h / screen_height
scaler = .90
surface_width, surface_height = int((phone_w / screen_scaler) * scaler), int((phone_h / screen_scaler) * scaler)
surface = pygame.display.set_mode((surface_width, surface_height))

# window caption, clock speed
pygame.display.set_caption("moving_doors_concept1")
clock = pygame.time.Clock()
fps = 60
# clock.tick(fps)

# colors
white = (255, 255, 255)
black = (0, 0, 0)
lightgrey = (150, 150, 150)
darkgrey = (100, 100, 100)
red = (255, 0, 0)

wall_thickness = 10


class Doors:
    def __init__(self):
        self.width_TB = (surface_width // 2) - 1
        self.height_TB = surface_height // wall_thickness
        self.width_LR = surface_height // wall_thickness
        self.height_LR = (surface_width // 2) - 1

        # top doors
        self.x_T_L = 0
        self.y_T_L = 0
        self.x_T_R = (surface_width // 2) + 1
        self.y_T_R = 0
        self.rect_T_L = pygame.Rect(self.x_T_L, self.y_T_L, self.width_TB, self.height_TB)
        self.rect_T_R = pygame.Rect(self.x_T_R, self.y_T_R, self.width_TB, self.height_TB)
        self.direction_T = 0
        self.rest_period_T = 0
        self.rest_T = True

        # bottom doors
        self.x_B_L = 0
        self.y_B_L = surface_height - (surface_height // wall_thickness)
        self.x_B_R = (surface_width // 2) + 1
        self.y_B_R = surface_height - (surface_height // wall_thickness)
        self.rect_B_L = pygame.Rect(self.x_B_L, self.y_B_L, self.width_TB, self.height_TB)
        self.rect_B_R = pygame.Rect(self.x_B_R, self.y_B_R, self.width_TB, self.height_TB)
        self.direction_B = 0
        self.rest_period_B = 0
        self.rest_B = True

        # left doors
        self.x_L_T = 0
        self.y_L_T = 0
        self.x_L_B = 0
        self.y_L_B = (surface_height // 2) + 1
        self.rect_L_T = pygame.Rect(self.x_L_T, self.y_L_T, self.width_LR, self.height_LR)
        self.rect_L_B = pygame.Rect(self.x_L_B, self.y_L_B, self.width_LR, self.height_LR)
        self.direction_L = 0
        self.rest_period_L = 0
        self.rest_L = True

        # right doors
        self.x_R_T = surface_width - self.width_LR
        self.y_R_T = 0
        self.x_R_B = surface_width - self.width_LR
        self.y_R_B = (surface_height // 2) + 1
        self.rect_R_T = pygame.Rect(self.x_R_T, self.y_R_T, self.width_LR, self.height_LR)
        self.rect_R_B = pygame.Rect(self.x_R_B, self.y_R_B, self.width_LR, self.height_LR)
        self.direction_R = 0
        self.rest_period_R = 0
        self.rest_R = True

        self.speed = 60
        self.switcher = None

    def slide_T(self):
        if self.rest_T:
            self.rest_period_T += 1
            if self.rest_period_T > 50:
                self.rest_T = False
        if not self.rest_T:
            if self.direction_T == 0:
                result_t = random.randint(1, 100)
                if result_t == 1:
                    self.direction_T = 1
                    if self.switcher is None:
                        self.switcher = "top"
                    else:
                        self.rest_T = True
                        self.rest_period_T = 0
                        self.direction_T = 0
            if self.switcher == "top":
                if self.rect_T_L.right > 0 and self.direction_T == 1:
                    self.rect_T_L.x -= self.speed
                    self.rect_T_R.x += self.speed

                    if self.rect_T_L.right <= 0:
                        self.direction_T = -1

                if self.rect_T_L.left < 0 and self.direction_T == -1:
                    self.rect_T_L.x += self.speed
                    self.rect_T_R.x -= self.speed

                    if self.rect_T_L.left == 0:
                        self.direction_T = 0
                        self.rest_T = True
                        self.rest_period_T = 0
                        self.switcher = None

    def slide_B(self):
        if self.rest_B:
            self.rest_period_B += 1
            if self.rest_period_B > 50:
                self.rest_B = False
        if not self.rest_B:
            if self.direction_B == 0:
                result_b = random.randint(1, 100)
                if result_b == 1:
                    self.direction_B = 1
                    if self.switcher is None:
                        self.switcher = "bottom"
                    else:
                        self.rest_B = True
                        self.rest_period_B = 0
                        self.direction_B = 0
            if self.switcher == "bottom":
                if self.rect_T_L.right > 0 and self.direction_B == 1:
                    self.rect_B_L.x -= self.speed
                    self.rect_B_R.x += self.speed

                    if self.rect_B_L.right <= 0:
                        self.direction_B = -1

                if self.rect_B_L.left < 0 and self.direction_B == -1:
                    self.rect_B_L.x += self.speed
                    self.rect_B_R.x -= self.speed

                    if self.rect_B_L.left == 0:
                        self.direction_B = 0
                        self.rest_B = True
                        self.rest_period_B = 0
                        self.switcher = None

    def slide_L(self):
        if self.rest_L:
            self.rest_period_L += 1
            if self.rest_period_L > 50:
                self.rest_L = False
        if not self.rest_L:
            if self.direction_L == 0:
                result_l = random.randint(1, 100)
                if result_l == 1:
                    self.direction_L = 1
                    if self.switcher is None:
                        self.switcher = "left"
                    else:
                        self.rest_L = True
                        self.rest_period_L = 0
                        self.direction_L = 0
            if self.switcher == "left":
                if self.rect_L_T.bottom > 0 and self.direction_L == 1:
                    self.rect_L_T.y -= self.speed
                    self.rect_L_B.y += self.speed

                    if self.rect_L_T.bottom <= 0:
                        self.direction_L = -1

                if self.rect_L_T.top < 0 and self.direction_L == -1:
                    self.rect_L_T.y += self.speed
                    self.rect_L_B.y -= self.speed

                    if self.rect_L_T.top == 0:
                        self.direction_L = 0
                        self.rest_L = True
                        self.rest_period_L = 0
                        self.switcher = None

    def slide_R(self):
        if self.rest_R:
            self.rest_period_R += 1
            if self.rest_period_R > 50:
                self.rest_R = False
        if not self.rest_R:
            if self.direction_R == 0:
                result_r = random.randint(1, 100)
                if result_r == 1:
                    self.direction_R = 1
                    if self.switcher is None:
                        self.switcher = "right"
                    else:
                        self.rest_R = True
                        self.rest_period_R = 0
                        self.direction_R = 0
            if self.switcher == "right":
                if self.rect_R_T.bottom > 0 and self.direction_R == 1:
                    self.rect_R_T.y -= self.speed
                    self.rect_R_B.y += self.speed

                    if self.rect_R_T.bottom <= 0:
                        self.direction_R = -1

                if self.rect_R_T.top < 0 and self.direction_R == -1:
                    self.rect_R_T.y += self.speed
                    self.rect_R_B.y -= self.speed

                    if self.rect_R_T.top == 0:
                        self.direction_R = 0
                        self.rest_R = True
                        self.rest_period_R = 0
                        self.switcher = None

    def draw(self):
        pygame.draw.rect(surface, black, self.rect_T_L)
        pygame.draw.rect(surface, black, self.rect_T_R)
        pygame.draw.rect(surface, black, self.rect_B_L)
        pygame.draw.rect(surface, black, self.rect_B_R)
        pygame.draw.rect(surface, black, self.rect_L_T)
        pygame.draw.rect(surface, black, self.rect_L_B)
        pygame.draw.rect(surface, black, self.rect_R_T)
        pygame.draw.rect(surface, black, self.rect_R_B)


doors = Doors()


while True:
    clock.tick(fps)
    surface.fill(lightgrey)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    doors.slide_T()
    doors.slide_B()
    doors.slide_L()
    doors.slide_R()
    doors.draw()

    pygame.display.update()