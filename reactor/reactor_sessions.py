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
            self.y_adjust = 100 * scaler
            self.rows_amount = 10
            self.row_size = (self.height - self.y_adjust) // self.rows_amount
            self.gridline_width = 1
            self.gridline_color = color.darkgrey
            self.radius = 8 * scaler

        def draw_graph(self, cols):
            if menu1.last_selected not in [0, 13, 14]:
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

        def draw_point(self, category, y_adjust, cols, render_type):

            col_size = (self.width - self.x_adjust) / cols
            data = all_data[menu2.last_selected][category]

            def color_grad(y_color_value):

                g = 255 - int(y_color_value * .2)
                if g <= 0:
                    g = 1

                if int(y_color_value * .2) <= 255:
                    r = int(y_color_value * .2)
                else:
                    r = int(y_color_value * .1)
                    if r > 255:
                        r = 255

                b = 0
                # print(r, g, b)
                return r, g, b

            # self.y = Point.y_adjust + (self.speed - fastest_time) * ((surface_height - (margin * 3)) / fast_slow_range)

            if render_type == 1:
                #  1 2 3 4 5 8 9 10 11 12 15 16
                try:
                    fastest = min([item for item in data if item != 0])  # 176.3
                    slowest = max([item for item in data if item != 0])  # 210.15
                except ValueError:
                    fastest, slowest = self.y_adjust, self.y_adjust  # 50, 50

                data_font_style = "/Users/thejourneyville/Documents/vscode/python/reactor/reactor/Instruction.ttf"

                for idx in range(cols):
                    if data[idx]:
                        if category not in [8, 9, 10, 11, 12, 15, 16]:
                            speed = int(data[idx])  # 176.3

                            try:
                                y_axis = self.y_adjust + (speed - fastest) * (
                                            (surface_height - self.y_adjust * 2) / (slowest - fastest))
                            except ZeroDivisionError:
                                y_axis = self.y_adjust

                            pygame.draw.circle(surface, color_grad(y_axis),
                                (self.x_adjust // 2 + (col_size // 2) + int(col_size * idx), y_axis), self.radius, 0)

                            item_font = pygame.font.Font(f"{data_font_style}", int(15 * scaler))
                            item_value_surface = item_font.render(str(round(data[idx], 2)), True, color.white)
                            item_value_rect = item_value_surface.get_rect()
                            item_value_rect.center = (((self.x_adjust // 2) + col_size // 2) + int(col_size * idx),
                                                      y_axis + 15)
                            surface.blit(item_value_surface, item_value_rect)
                        else:

                            speed = int(data[idx])
                            try:
                                y_axis = surface_height - (self.y_adjust + (speed - fastest) * (
                                            (surface_height - self.y_adjust * 2) / (slowest - fastest)))
                            except ZeroDivisionError:
                                y_axis = self.y_adjust

                            if y_axis <= 25:
                                y_axis = 50

                            pygame.draw.circle(surface, color_grad(y_axis),
                                (((self.x_adjust // 2) + col_size // 2) + int(col_size * idx), y_axis), self.radius, 0)

                            item_font = pygame.font.Font(f"{data_font_style}", int(15 * scaler))
                            item_value_surface = item_font.render(str(round(data[idx], 2)), True, color.white)
                            item_value_rect = item_value_surface.get_rect()
                            item_value_rect.center = (((self.x_adjust // 2) + col_size // 2) + int(col_size * idx),
                                                      y_axis + 15)
                            surface.blit(item_value_surface, item_value_rect)

            if render_type == 0:
                # 0 6 7 13 14

                try:
                    fastest = min([item for item in
                                   [item if not isinstance(item, tuple) else item[-1] for item in data] if item != 0])
                    slowest = max([item for item in
                                   [item if not isinstance(item, tuple) else item[-1] for item in data] if item != 0])
                except ValueError:
                    fastest, slowest = self.y_adjust, self.y_adjust

                data_font_style = "/Users/thejourneyville/Documents/vscode/python/reactor/reactor/Instruction.ttf"
                directions = ["NA", "U", "D", "L", "R"]

                for idx, item in enumerate(data):
                    item_font = pygame.font.Font(f"{data_font_style}", int(10 * scaler))

                    if category == 6 or category == 7:  # fastest directions

                        speed = int(item[-1])
                        color_code = ["NA", "up", "down", "left", "right"]

                        try:
                            y_axis = self.y_adjust + (speed - fastest) * (
                                            (surface_height - self.y_adjust * 2) / (slowest - fastest))
                        except ZeroDivisionError:
                            y_axis = self.y_adjust

                        print(f"sessions: category 6 or 7: item: {item}")

                        item_direction_surface = item_font.render(item[0][0], True, color.stats[color_code.index(item[0])])
                        item_value_surface = item_font.render(str(round(item[-1], 2)), True, color.white)
                        item_direction_rect = item_direction_surface.get_rect()
                        item_value_rect = item_value_surface.get_rect()
                        item_direction_rect.center = (((self.x_adjust // 2) + col_size // 2) + int(col_size * idx),
                                                      y_axis)
                        item_value_rect.center = (((self.x_adjust // 2) + col_size // 2) + int(col_size * idx),
                                                  y_axis + 15)
                        surface.blit(item_direction_surface, item_direction_rect)
                        surface.blit(item_value_surface, item_value_rect)

                    if category == 13 or category == 14:  # worst
                        item_surface = item_font.render(directions[item], True, color.white)
                    else:
                        item_surface = item_font.render(str(item), True, color.white)
                    if category not in [6, 7]:
                        item_rect = item_surface.get_rect()
                        item_rect.center = (((self.x_adjust // 2) + col_size // 2) + int(col_size * idx), self.height // 2)

                        surface.blit(item_surface, item_rect)

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
            self.last_selected = 0
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
                                    self.title_initialized = False
                                    # print(self.last_selected, categories[self.floating_over_items - 1])
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

            header_font_style = "/Users/thejourneyville/Documents/vscode/python/reactor/reactor/darkforest.ttf"
            data_font_style = "/Users/thejourneyville/Documents/vscode/python/reactor/reactor/Instruction.ttf"

            def menu_title():
                text_y_adjust = 2 * scaler
                if not self.title_initialized:
                    self.name_font = pygame.font.Font(f"{header_font_style}", int(20 * scaler))
                    if menu == menu1:
                        self.name_surface = self.name_font.render(categories[self.last_selected], True, self.text_color)
                    else:
                        self.name_surface = self.name_font.render(date_ranges[self.last_selected], True, self.text_color)
                    self.name_rect = self.name_surface.get_rect()
                    self.name_rect.center = self.x_adjust + self.menu_width // 2,\
                                            self.y_adjust + self.row_height // 2 + text_y_adjust
                    self.title_initialized = True

                surface.blit(self.name_surface, self.name_rect)

            def data():
                text_y_adjust = -1 * scaler
                colors = [(255, 255, 255), (0, 0, 0)]
                if not self.data_initialized:
                    self.data_font = pygame.font.Font(f"{data_font_style}", int(15 * scaler))
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

        category1 = [0, 6, 7, 13, 14] # string related
        category2 = [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16]  # integer related
        category_group = None

        if category in category1:
            category_group = 0
        elif category in category2:
            category_group = 1

        if category not in [6, 7, 13, 14]:
            try:
                adjuster = (surface_height - graph.y_adjust) / max(all_data[time_range][category])
            except ZeroDivisionError:
                adjuster = 0

        elif category in [6, 7]:
            speeds = max([int(i[-1]) for i in all_data[time_range][category]])
            adjuster = (surface_height - graph.y_adjust) / speeds

        else:
            adjuster = 0

        graph_columns = len(all_data[time_range][category])

        return adjuster, graph_columns, category_group

    categories = ['level',
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
                  'common wrong launch direction',
                  'common mistook door',
                  'assertion',
                  'time elapsed',
              ]

    date_ranges = ['today',
                   'day average',
                   'week average',
                   'month average',
                   ]

    # LEGEND:
    # menu name / number of rows / menu width, row height / x_axis start point, y_axis start point, data, float_color
    menu1 = DropDown(str("session"), len(categories), 387, 20, 0, 0, categories, (33, 139, 71))
    menu2 = DropDown(str("range"), len(date_ranges), 170, 20, 388, 0, date_ranges, (32, 125, 255))

    menus = (menu1, menu2)

    all_data = sessions_data.retrieve(player)

    def test1(data1):

        print("TEST:")
        print(f"name: all_data\nsize: {len(data1[0])}\nlayer0: {data1}")
        input()

    # test1(all_data)

    graph = Graph()

    while True:

        clock.tick(fps)
        surface.fill(color.black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        if all([menu1.last_selected is not None,
                menu2.last_selected is not None]):
            y_adjuster, cols_amount, category_type = processing(menu1.last_selected, menu2.last_selected)

            graph.draw_graph(cols_amount)
            # print(f"menu1.last_selected: {menu1.last_selected}, y_adjuster: {y_adjuster}, cols_amount: {cols_amount}, category_type: {category_type}")
            graph.draw_point(menu1.last_selected, y_adjuster, cols_amount, category_type)

        mx, my = pygame.mouse.get_pos()

        for menu in menus:
            menu.mouse_timer += 1
            menu.activate()
            menu.draw_menu()
            menu.highlight()
            menu.menu_text()

        pygame.display.update()

