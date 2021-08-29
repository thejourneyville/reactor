import pygame
from reactor_database import database


def sessions(surface, scaler, clock, fps, player, level, session_data, assertion, time_elapsed):

    # window caption
    pygame.display.set_caption("REACTOR SESSIONS")

    class DropDown:
        def __init__(self, menu_name, rows, menu_width, row_height, x_adjust, y_adjust, data):
            self.menu_name = menu_name
            self.rows = rows
            self.data = data
            self.data_initialize = True
            self.data_font = None
            self.data_surfaces = None
            self.data_rects = None
            self.x_adjust = x_adjust * scaler
            self.y_adjust = y_adjust * scaler
            self.menu_width = menu_width * scaler
            self.row_height = row_height * scaler
            self.menu_height = self.row_height * self.rows
            self.background_color = (50, 50, 50)
            self.menu_bar_color = (75, 75, 75)
            self.checkbox_outline_color = (0, 0, 0)
            self.float_color = (0, 0, 200)
            self.text_color = (200, 200, 200)
            self.text_float_color = (0, 0, 0)
            self.activated_color = (200, 200, 200)
            self.mouse_timer = 20
            self.menu_activated = False
            self.floating_over_items = None
            self.menu_slide_position = 0
            self.menu_slide_speed = 50 * scaler
            self.menu_rect = pygame.Rect(self.x_adjust, self.y_adjust, self.menu_width, self.row_height)
            self.menu_checkbox_rect = pygame.Rect(self.x_adjust + 2, self.y_adjust + 2, self.row_height - 4,
                                                  self.row_height - 4)
            self.menu_checkbox_rect_outline = pygame.Rect(self.x_adjust + 1, self.y_adjust + 1, self.row_height - 3,
                                                          self.row_height - 3)
            self.expand_triangle = (
                (self.x_adjust + 4, self.y_adjust + 4), (self.x_adjust + self.row_height - 6, self.y_adjust + 4),
                (self.x_adjust + (self.row_height - 2.5) // 2, self.y_adjust + self.row_height - 6))
            self.contract_triangle = ((self.x_adjust + 4, self.y_adjust + self.row_height - 6),
                                      (self.x_adjust + self.row_height - 6, self.y_adjust + self.row_height - 6),
                                      (self.x_adjust + (self.row_height - 2.5) // 2, self.y_adjust + 4))

        def draw_menu(self):

            pygame.draw.rect(surface, self.menu_bar_color, self.menu_rect)

            if self.menu_activated:
                pygame.draw.rect(surface, self.background_color,
                    (self.x_adjust, self.y_adjust + self.row_height, self.menu_width, self.menu_slide_position))

                if self.menu_slide_position < self.menu_height:
                    if self.menu_height - self.menu_slide_position < self.menu_slide_speed:
                        self.menu_slide_position += self.menu_height - self.menu_slide_position
                    else:
                        self.menu_slide_position += self.menu_slide_speed
                else:
                    self.menu_slide_position = self.menu_height

                pygame.draw.rect(surface, self.activated_color, self.menu_checkbox_rect, 0)

                if self.menu_slide_position == self.menu_height:
                    for line in range(1, self.rows + 1):
                        pygame.draw.line(surface, (0, 0, 0), (self.x_adjust, self.y_adjust + self.row_height * line),
                            (self.x_adjust + self.menu_width - 1, self.y_adjust + self.row_height * line))
            else:
                if self.menu_slide_position > 0:
                    pygame.draw.rect(surface, self.background_color,
                        (self.x_adjust, self.y_adjust + self.row_height, self.menu_width, self.menu_slide_position))
                    self.menu_slide_position -= self.menu_slide_speed
                else:
                    self.menu_slide_position = 0

            pygame.draw.rect(surface, self.checkbox_outline_color, self.menu_checkbox_rect_outline, 1)

        def highlight(self):

            if self.menu_activated:

                for row in range(1, self.rows + 1):
                    if self.x_adjust < mx < self.x_adjust + self.menu_width:
                        if self.y_adjust + self.row_height * row < my < self.y_adjust + self.row_height * row + self.row_height:

                            self.floating_over_items = row
                            if self.mouse_timer >= 20:
                                if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                                    print(self.data[self.floating_over_items - 1])
                                    self.mouse_timer = 0
                                    self.menu_activated = False

                            pygame.draw.rect(surface, self.float_color,
                                [self.x_adjust, (self.y_adjust + (self.row_height * self.floating_over_items)),
                                 self.menu_width, self.row_height - 1])
                else:
                    self.floating_over_items = None

            if self.x_adjust < mx < self.x_adjust + self.row_height:
                if self.y_adjust < my < self.y_adjust + self.row_height:
                    if not self.menu_activated:
                        pygame.draw.polygon(surface, (0, 0, 0), self.expand_triangle)
                    else:
                        pygame.draw.polygon(surface, (0, 0, 0), self.contract_triangle, 1)

        def activate(self):
            if self.x_adjust < mx < self.x_adjust + self.row_height:
                if self.y_adjust < my < self.y_adjust + self.row_height:
                    if self.mouse_timer >= 20:
                        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                            if not self.menu_activated:
                                self.menu_activated = True
                            else:
                                self.menu_activated = False
                            self.mouse_timer = 0

        def menu_text(self):

            name_font_style = "Instruction.ttf"

            def menu_title():
                name_font = pygame.font.Font(f"./{name_font_style}", int(20 * scaler))
                name_surface = name_font.render(self.menu_name, True, self.text_color)
                name_rect = name_surface.get_rect()
                name_rect.center = self.x_adjust + self.menu_width // 2, self.y_adjust + self.row_height // 2

                surface.blit(name_surface, name_rect)

            def data():
                if self.data_initialize:
                    self.data_font = pygame.font.Font(f"./{name_font_style}", int(20 * scaler))
                    self.data_surfaces = [self.data_font.render(item, True, self.text_color) for item in self.data]
                    self.data_rects = [data_surface.get_rect() for data_surface in self.data_surfaces]

                    for idx, item in enumerate(self.data_rects):
                        item.left, item.centery = self.x_adjust + self.row_height, self.y_adjust + (
                                self.row_height * (idx + 1) + self.row_height // 2)
                    self.data_initialize = False
                else:
                    for idx, item in enumerate(self.data_rects):
                        surface.blit(self.data_surfaces[idx], item)

            menu_title()
            if self.menu_slide_position == self.menu_height:
                data()


    # title = input("enter title: ")
    # items = [item for item in input("enter items: ").split()]
    player = "benny"
    items = ["this", "is", "a", "test", "to", "see", "what", "happens"]

    # LEGEND: menu name / number of rows / menu width, row height / x_axis start point, y_axis start point, data

    labels = ['name',
              'level'
              'up success reaction times average',
              'down success reaction times average',
              'left success reaction times average',
              'right success reaction times average',
              'total success reaction times average',
              'fastest direction success average',
              'slowest direction success average',
              'up shots percentage',
              'down shots percentage',
              'left shots percentage',
              'right shots percentage',
              'total shots percentage',
              'worst wrong launch direction',
              'worst mistook door',
              'most common wrong scenarios',
              'assertion',
              'time elapsed',
              ]

    menu = DropDown(f"{player}: session data", len(labels), 400, 20, 0, 0, labels)

    while True:

        clock.tick(fps)
        surface.fill((200, 200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    break

        mx, my = pygame.mouse.get_pos()
        menu.mouse_timer += 1

        menu.activate()
        menu.draw_menu()
        menu.highlight()
        menu.menu_text()

        pygame.display.update()


