import pygame

# initializing pygame
pygame.init()

# screen/surface setup:
width, height = 1, 1  # screen aspect ratio
display_info_object = pygame.display.Info()
screen_width, screen_height = display_info_object.current_w, display_info_object.current_h
screen_scaler = height / screen_height
scaler = .75
surface_width, surface_height = int((width / screen_scaler) * scaler), int((height / screen_scaler) * scaler)
surface = pygame.display.set_mode((surface_width, surface_height))

# window caption, clock speed
pygame.display.set_caption("REACTOR MENU")
clock = pygame.time.Clock()
fps = 60


class DropDown:
    def __init__(self, rows, data):
        self.rows = rows
        self.data = data
        self.size_x = surface_width // 3
        self.size_y = 40 * scaler
        self.size_open_y = self.size_y * self.rows
        self.pos_x = 0
        self.pos_y = 1
        self.background_color = (25, 25, 25)
        self.menu_bar_color = (50, 50, 50)
        self.checkbox_outline_color = (200, 200, 200)
        self.float_color = (0, 0, 200)
        self.text_color = (200, 200, 200)
        self.text_float_color = (0, 0, 0)
        self.activated_color = (0, 0, 255)
        self.floating_over = None
        self.menu_rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)
        self.menu_checkbox_rect = pygame.Rect(self.pos_x, self.pos_y + 1, self.size_y, self.size_y - 1)
        self.menu_open_rect = pygame.Rect(self.pos_x, self.size_y, self.size_x, self.size_open_y)
        self.highlight_bar = pygame.Rect(self.pos_x, self.size_y * 3, self.size_x, self.size_y) # dynamic position

    def draw_menu(self, activated):
        pygame.draw.rect(surface, self.menu_bar_color, self.menu_rect)
        if activated:
            pygame.draw.rect(surface, self.background_color, self.menu_open_rect)
            for line in range(1, self.rows + 1):
                pygame.draw.line(surface, (0, 0, 0), (self.pos_x, self.size_y * line), (self.size_x - 1, self.size_y * line))
        pygame.draw.rect(surface, self.checkbox_outline_color, self.menu_checkbox_rect, 1)

    def highlighted(self, mouse_x, mouse_y):
        for row in range(1, self.rows + 1):
            if self.pos_x <= mouse_x <= self.size_x:
                if self.size_y * row <= mouse_y <= self.size_y * row + self.size_y:
                    self.floating_over = row
                    pygame.draw.rect(surface, self.float_color,
                        [self.pos_x, (1 + self.size_y * self.floating_over), self.size_x, self.size_y])
        else:
            self.floating_over = None





menu = DropDown(8, ["apple", "pear", "miso soup"])

while True:

    clock.tick(fps)
    surface.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    mx, my = pygame.mouse.get_pos()

    menu.draw_menu(1)
    menu.highlighted(mx, my)




    pygame.display.update()