import pygame

# initializing pygame
pygame.init()

# screen/surface setup:
width, height = 1, 1  # screen aspect ratio
display_info_object = pygame.display.Info()
screen_width, screen_height = display_info_object.current_w, display_info_object.current_h
screen_scaler = height / screen_height
scaler = 4
surface_width, surface_height = int((width / screen_scaler) * scaler), int((height / screen_scaler) * scaler)
surface = pygame.display.set_mode((surface_width, surface_height))

# window caption, clock speed
pygame.display.set_caption("REACTOR MENU")
clock = pygame.time.Clock()
fps = 60


class DropDown:
    def __init__(self, name, rows, size_x, size_y, data):
        self.name                       = name
        self.rows                       = rows
        self.data                       = data
        self.size_x                     = size_x * scaler
        self.size_y                     = size_y * scaler
        self.size_open_y                = self.size_y * self.rows
        self.pos_x                      = 0
        self.pos_y                      = 1
        self.background_color           = (50, 50, 50)
        self.menu_bar_color             = (75, 75, 75)
        self.checkbox_outline_color     = (0, 0, 0)
        self.float_color                = (0, 0, 200)
        self.text_color                 = (200, 200, 200)
        self.text_float_color           = (0, 0, 0)
        self.activated_color            = (200, 200, 200)
        self.mouse_timer                = 0
        self.activated                  = False
        self.floating_over_items        = None
        self.menu_slide_position        = 0
        self.menu_slide_speed           = 50
        self.menu_rect                  = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y - 1)
        self.menu_open_rect             = pygame.Rect(self.pos_x, self.size_y, self.size_x, self.menu_slide_position)
        self.menu_checkbox_rect         = pygame.Rect(self.pos_x + 2, self.pos_y + 2, self.size_y - 4, self.size_y - 4)
        self.menu_checkbox_rect_outline = pygame.Rect(self.pos_x + 1, self.pos_y + 1, self.size_y - 3, self.size_y - 3)
        self.expand_triangle            =           ((self.pos_x + 4, self.pos_y + 4),
                                                     (self.size_y - 6, self.pos_y + 4),
                                                    ((self.size_y - 2.5) // 2, self.size_y - 4))
        self.contract_triangle          =           ((self.pos_x + 4, self.size_y - 4),
                                                     (self.size_y - 6, self.size_y - 4),
                                                    ((self.size_y - 2.5) // 2, self.pos_y + 4))

    def draw_menu(self):

        pygame.draw.rect(surface, self.menu_bar_color, self.menu_rect)

        if self.activated:
            pygame.draw.rect(surface, self.background_color, (self.pos_x, self.size_y, self.size_x, self.menu_slide_position))
            if self.menu_slide_position < self.size_open_y:
                if self.size_open_y - self.menu_slide_position < self.menu_slide_speed:
                    self.menu_slide_position += self.size_open_y - self.menu_slide_position
                else:
                    self.menu_slide_position += self.menu_slide_speed
            else:
                self.menu_slide_position = self.size_open_y

            pygame.draw.rect(surface, self.activated_color, self.menu_checkbox_rect, 0)

            for line in range(1, self.rows + 1):
                pygame.draw.line(surface, (0, 0, 0), (self.pos_x, self.size_y * line),
                                                     (self.size_x - 1, self.size_y * line))
        else:

            if self.menu_slide_position > 0:
                pygame.draw.rect(surface, self.background_color,
                                 (self.pos_x, self.size_y, self.size_x, self.menu_slide_position))
                self.menu_slide_position -= self.menu_slide_speed
            else:
                self.menu_slide_position = 0

        pygame.draw.rect(surface, self.checkbox_outline_color, self.menu_checkbox_rect_outline, 1)

    def highlight(self):

        if self.activated:

            for row in range(1, self.rows + 1):
                if self.pos_x < mx < self.size_x:
                    if self.size_y * row < my < self.size_y * row + self.size_y:

                        self.floating_over_items = row
                        if self.mouse_timer >= 20:
                            if pygame.mouse.get_pressed() == (1, 0, 0):
                                print(self.data[self.floating_over_items - 1])
                                self.mouse_timer = 0
                                self.activated = False

                        pygame.draw.rect(surface, self.float_color,
                                         [self.pos_x, (self.pos_y + (self.size_y * self.floating_over_items)),
                                          self.size_x, self.size_y - 1])
            else:
                self.floating_over_items = None

        if self.pos_x < mx < self.size_y:
            if self.pos_y < my < self.size_y:

                if not self.activated:
                    pygame.draw.polygon(surface, (0, 0, 0), self.expand_triangle)
                else:
                    pygame.draw.polygon(surface, (0, 0, 0), self.contract_triangle, 1)

    def activate(self):
        if self.pos_x < mx < self.size_y:
            if self.pos_y < my < self.size_y:
                if self.mouse_timer >= 20:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        if not self.activated:
                            self.activated = True
                        else:
                            self.activated = False
                        self.mouse_timer = 0
        # else:
        #     if self.floating_over_items is not None:
        #         print("here")
        #         if self.mouse_timer >= 20:
        #             if pygame.mouse.get_pressed() == (1, 0, 0):
        #                 print(self.floating_over_items)
        #                 self.mouse_timer = 0
        #                 self.activated = False

    def menu_text(self):

        name_font_style = "darkforest.ttf"

        def menu_title():
            name_font                   = pygame.font.Font(f"./{name_font_style}", 20 * scaler)
            name_surface                = name_font.render(self.name, True, self.text_color)
            name_rect                   = name_surface.get_rect()
            name_rect.center            = self.size_x // 2, self.pos_y + self.size_y // 2

            surface.blit(name_surface, name_rect)

        def data():
            name_font                   = pygame.font.Font(f"./{name_font_style}", 20 * scaler)
            name_surfaces               = [name_font.render(item, True, self.text_color) for item in self.data]
            name_rects                  = [name_surface.get_rect() for name_surface in name_surfaces]

            for idx, item in enumerate(name_rects):
                item.left, item.centery = self.pos_x + self.size_y, \
                                          self.pos_y + (self.size_y * (idx + 1) + self.size_y // 2)

                surface.blit(name_surfaces[idx], item)

        menu_title()
        if self.menu_slide_position == self.size_open_y:
            data()

# title = input("enter title: ")
# items = [item for item in input("enter items: ").split()]
items = ["this", "is", "a", "test", "to", "see", "what", "happens"]

menu = DropDown("something", len(items), 300, 20, items)

while True:

    clock.tick(fps)
    surface.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    mx, my = pygame.mouse.get_pos()
    menu.mouse_timer += 1

    menu.activate()
    menu.draw_menu()
    menu.highlight()
    menu.menu_text()

    pygame.display.update()
