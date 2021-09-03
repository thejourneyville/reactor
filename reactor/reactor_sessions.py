import pygame
import reactor_sessions_data as sessions_data
import reactor_colors as color


def sessions(surface, surface_width, surface_height, scaler, clock, fps, player):

    # window caption
    pygame.display.set_caption("REACTOR SESSIONS")

    # NOTE: processing function will take selected data, pass it's size to Graph for number of cols/rows?

    class Graph:
        def __init__(self):
            self.width = surface_width
            self.height = surface_height
            self.x_adjust = 50 * scaler
            self.y_adjust = 50 * scaler
            self.rows_amount = 10
            self.row_size = (self.height - self.y_adjust) // self.rows_amount
            self.gridline_width = 1
            self.gridline_color = color.lighter_grey

        def draw_graph(self, cols):
            for row in range(self.rows_amount + 1):
                # rows
                pygame.draw.line(
                    surface,
                    self.gridline_color,
                    (self.x_adjust // 2, (self.y_adjust // 2) + int(self.row_size * row)),
                    (surface_width - self.x_adjust // 2, (self.y_adjust // 2) + int(self.row_size * row)),
                    self.gridline_width)

            col_size = (self.width - self.x_adjust) / cols
            for col in range(cols + 1):
                # cols
                pygame.draw.line(
                    surface,
                    self.gridline_color,
                    ((self.x_adjust // 2) + int(col_size * col), self.y_adjust // 2),
                    ((self.x_adjust // 2) + int(col_size * col), self.height - self.y_adjust // 2),
                    self.gridline_width)

        def draw_point(self, category, y_adjust, cols):

            data = all_data[category]
            for idx in range(cols + 1):
                pygame.draw.circle(surface, color.alert_red,
                    ((self.x_adjust // 2) + self.x, self.reaction_time), self.radius, self.result)

    class DropDown:
        def __init__(self, menu_name, rows, menu_width, row_height, x_adjust, y_adjust, data, float_color):
            self.menu_name = menu_name
            self.rows = rows
            self.data = data
            self.data_initialized = False
            self.data_font = None
            self.data_surfaces = None
            self.data_rects = None
            self.title_initialized = False
            self.name_font = None
            self.name_surface = None
            self.name_rect = None
            self.x_adjust = x_adjust * scaler
            self.y_adjust = y_adjust * scaler
            self.menu_width = menu_width * scaler
            self.row_height = row_height * scaler
            self.menu_height = self.row_height * self.rows
            self.background_color = (50, 50, 50)
            self.menu_bar_color = (75, 75, 75)
            self.checkbox_outline_color = (0, 0, 0)
            self.float_color = float_color
            self.text_color = (255, 255, 255)
            self.activated_color = (200, 200, 200)
            self.mouse_timer = 20
            self.menu_activated = False
            self.floating_over_items = None
            self.last_selected = None
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
                        if self.y_adjust + self.row_height * row < my < \
                                self.y_adjust + self.row_height * row + self.row_height:

                            self.floating_over_items = row
                            if self.mouse_timer >= 20:
                                if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                                    self.last_selected = self.floating_over_items - 1
                                    print(self.last_selected)
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

            header_font_style = "darkforest.ttf"
            data_font_style = "Instruction.ttf"

            def menu_title():
                text_y_adjust = 2 * scaler
                if not self.title_initialized:
                    self.name_font = pygame.font.Font(f"./{header_font_style}", int(20 * scaler))
                    self.name_surface = self.name_font.render(self.menu_name, True, self.text_color)
                    self.name_rect = self.name_surface.get_rect()
                    self.name_rect.center = self.x_adjust + self.menu_width // 2,\
                                            self.y_adjust + self.row_height // 2 + text_y_adjust
                    self.title_initialized = True

                surface.blit(self.name_surface, self.name_rect)

            def data():
                text_y_adjust = -1 * scaler
                colors = [(255, 255, 255), (0, 0, 0)]
                if not self.data_initialized:
                    self.data_font = pygame.font.Font(f"./{data_font_style}", int(15 * scaler))
                    self.data_surfaces = [self.data_font.render(category, True, colors[0]) for category in self.data]
                    self.data_rects = [data_surface.get_rect() for data_surface in self.data_surfaces]

                    for idx, item in enumerate(self.data_rects):
                        item.left, item.centery = self.x_adjust + self.row_height, self.y_adjust + (
                                self.row_height * (idx + 1) + self.row_height // 2 + text_y_adjust)
                    self.data_initialized = True

                for idx, item in enumerate(self.data_rects):
                    surface.blit(self.data_surfaces[idx], item)

            menu_title()
            if self.menu_slide_position == self.menu_height:
                data()

    def processing(category, time_range):

        if time_range == 0:

            adjuster = surface_height / max(all_data[category])
            graph_columns = len(all_data[category])

        else:
            adjuster = surface_height - max(all_data[category])
            graph_columns = len(all_data[category])

        return adjuster, graph_columns

    categories = [' 1 level',
                  ' 2 up success reaction times average',
                  ' 3 down success reaction times average',
                  ' 4 left success reaction times average',
                  ' 5 right success reaction times average',
                  ' 6 total success reaction times average',
                  ' 7 fastest direction success average',
                  ' 8 slowest direction success average',
                  ' 9 up shots percentage',
                  '10 down shots percentage',
                  '11 left shots percentage',
                  '12 right shots percentage',
                  '13 total shots percentage',
                  '14 worst wrong launch direction',
                  '15 worst mistook door',
                  '16 assertion',
                  '17 time elapsed',
              ]

    date_ranges = ['1 today',
                   '2 day average',
                   '3 week average',
                   '4 month average',
                   ]

    # LEGEND:
    # menu name / number of rows / menu width, row height / x_axis start point, y_axis start point, data, float_color
    menu1 = DropDown(str("session"), len(categories), 387, 20, 0, 0, categories, (33, 139, 71))
    menu2 = DropDown(str("range"), len(date_ranges), 170, 20, 388, 0, date_ranges, (32, 125, 255))
    menus = (menu1, menu2)

    all_data = sessions_data.retrieve(player)

    # def test1(data1):
    #
    #     print("TEST:")
    #     print(f"name: all_data\nsize: {len(data1[0])}\nlayer0: {data1}")
    #     input()
    #
    # test1(all_data)

    graph = Graph()

    while True:

        clock.tick(fps)
        surface.fill((200, 200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        if all([menu1.last_selected is not None,
                menu2.last_selected is not None]):
            y_adjuster, cols_amount = processing(menu1.last_selected, menu2.last_selected)

            graph.draw_graph(cols_amount)
            graph.draw_point(menu1.last_selected, y_adjuster, cols_amount)

        mx, my = pygame.mouse.get_pos()

        for menu in menus:
            menu.mouse_timer += 1
            menu.activate()
            menu.draw_menu()
            menu.highlight()
            menu.menu_text()

        pygame.display.update()

