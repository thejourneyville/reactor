import pygame
import random

# initializing pygame
pygame.init()

# screen/surface setup:
phone_w, phone_h = 1000, 1000
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



class LeftDoor:
    def __init__(self):
        self.width = (surface_width // 2) - 1
        self.height = surface_height // 16
        self.x = 0
        self.y = (surface_height // 2) - (surface_height // 16) // 2
        self.speed = 70
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
        self.rest = True
        self.rest_period = 0

    def slide(self):
        if self.rest:
            self.rest_period += 1
            if self.rest_period > 100:
                self.rest = False
        if not self.rest:
            if self.direction == 0:
                result = random.randint(1, 100)
                if result == 1:
                    self.direction = 1

            if self.rect.right > 0 and self.direction == 1:
                self.rect.x -= self.speed

                if self.rect.right <= 0:
                    self.direction = -1

            if self.rect.left < 0 and self.direction == -1:
                self.rect.x += self.speed

                if self.rect.left == 0:
                    self.direction = 0
                    self.rest = True
                    self.rest_period = 0


    def draw(self):
        pygame.draw.rect(surface, darkgrey, self.rect)


class RightDoor:
    def __init__(self):
        self.width = (surface_width // 2) + 1
        self.height = surface_height // 16
        self.x = surface_width // 2
        self.y = (surface_height // 2) - (surface_height // 16) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def slide(self, d):
        self.rect.x = self.x + (d.rect.x * -1)

    def draw(self):
        pygame.draw.rect(surface, darkgrey, self.rect)


class Marker:
    def __init__(self):
        self.diag1 = (0, surface_height), (surface_width, 0)
        self.diag2 = (0, 0), (surface_width, surface_height)

    def flash(self, d):
        if d.direction != 0:
            pygame.draw.polygon(surface, red, self.diag1, 1)
            pygame.draw.polygon(surface, red, self.diag2, 1)


Ldoor = LeftDoor()
Rdoor = RightDoor()
marker = Marker()


while True:
    clock.tick(fps)
    surface.fill((180, 180, 180))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    Ldoor.slide()
    Ldoor.draw()

    Rdoor.draw()
    Rdoor.slide(Ldoor)

    marker.flash(Ldoor)

    pygame.display.update()
