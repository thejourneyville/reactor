import pygame
import reactor_colors as color


def stats(surface, surface_width, surface_height, margin_color, scaler, clock, fps, level, current_react_data,
          time_elapsed):
    pygame.display.set_caption(f"PLAYER STATISTICS")
    margin = int(30 * scaler)

    if not current_react_data:
        return

    print(f"current_react_data: {current_react_data}")
    success_data    = [(entry[-1], entry[2], entry[0], False) for entry in current_react_data['success']]
    fail_data       = [(entry[-1], entry[2], entry[0], True) for entry in current_react_data['fail']]
    all_data        = success_data + fail_data
    slowest_time    = max([idx[1] for idx in all_data])
    fastest_time    = min([idx[1] for idx in all_data])

    up_data     = [(entry[0], entry[1]) for entry in all_data if entry[2] == 1]
    down_data   = [(entry[0], entry[1]) for entry in all_data if entry[2] == 2]
    left_data   = [(entry[0], entry[1]) for entry in all_data if entry[2] == 3]
    right_data  = [(entry[0], entry[1]) for entry in all_data if entry[2] == 4]
    line_data   = [up_data, down_data, left_data, right_data]

    class Graph:
        def __init__(self):
            self.width = surface_width
            self.height = surface_height
            self.x_adjust = margin / 2
            self.y_adjust = margin / 2
            self.row_amount = 20
            self.rows = (self.height - margin) / self.row_amount
            self.cols_amount = time_elapsed
            self.cols = (self.width - margin) / self.cols_amount
            self.gridline_width = 1
            self.gridline_color = color.darkgrey

        def draw_graph(self):
            for row in range(self.row_amount):
                # rows
                pygame.draw.line(
                    surface,
                    self.gridline_color,
                    (0, int(self.y_adjust + (self.rows * row))),
                    (surface_width, int(self.y_adjust + (self.rows * row))),
                    self.gridline_width)

            for col in range(int(self.cols_amount)):
                # cols
                pygame.draw.line(
                    surface,
                    self.gridline_color,
                    (int(self.y_adjust + (self.cols * col)), 0),
                    (int(self.y_adjust + (self.cols * col)), surface_height),
                    self.gridline_width)

    class Boxes:
        def __init__(self):
            self.size_x = 10 * scaler
            self.size_y = 10 * scaler
            self.press_up = True
            self.press_down = True
            self.press_left = True
            self.press_right = True
            self.mouse_timer = 0
            self.selected_up = True
            self.selected_down = True
            self.selected_left = True
            self.selected_right = True

        def draw_box(self, mouse_cords):

            fill_color_up, fill_color_down, fill_color_left, fill_color_right = \
                color.lightgrey, color.lightgrey, color.lightgrey, color.lightgrey
            fill_up, fill_down, fill_left, fill_right = 1, 1, 1, 1

            up_box = pygame.Rect(((margin + 35) * scaler, (margin - 7 * scaler), self.size_x, self.size_y))
            down_box = pygame.Rect(((margin + 35) * scaler, (margin + 13 * scaler), self.size_x, self.size_y))
            left_box = pygame.Rect(((margin + 35) * scaler, (margin + 33 * scaler), self.size_x, self.size_y))
            right_box = pygame.Rect(((margin + 35) * scaler, (margin + 53 * scaler), self.size_x, self.size_y))

            x_mouse = mouse_cords[0]
            y_mouse = mouse_cords[-1]
            self.mouse_timer += 1

            if up_box.left <= x_mouse <= (up_box.left + self.size_x):
                if up_box.top <= y_mouse <= (up_box.top + self.size_y):

                    if self.mouse_timer >= 10:
                        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                            self.mouse_timer = 0
                            if not self.press_up:
                                self.press_up = True
                                self.selected_up = True
                            else:
                                self.press_up = False
                                self.selected_up = False

                    fill_color_up = color.lighter_grey
                    fill_up = 0

            if down_box.left <= x_mouse <= (down_box.left + self.size_x):
                if down_box.top <= y_mouse <= (down_box.top + self.size_y):

                    if self.mouse_timer >= 10:
                        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                            self.mouse_timer = 0
                            if not self.press_down:
                                self.press_down = True
                                self.selected_down = True
                            else:
                                self.press_down = False
                                self.selected_down = False

                    fill_color_down = color.lighter_grey
                    fill_down = 0

            if left_box.left <= x_mouse <= (left_box.left + self.size_x):
                if left_box.top <= y_mouse <= (left_box.top + self.size_y):

                    if self.mouse_timer >= 10:
                        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                            self.mouse_timer = 0
                            if not self.press_left:
                                self.press_left = True
                                self.selected_left = True
                            else:
                                self.press_left = False
                                self.selected_left = False

                    fill_color_left = color.lighter_grey
                    fill_left = 0

            if right_box.left <= x_mouse <= (right_box.left + self.size_x):
                if right_box.top <= y_mouse <= (right_box.top + self.size_y):

                    if self.mouse_timer >= 10:
                        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                            self.mouse_timer = 0
                            if not self.press_right:
                                self.press_right = True
                                self.selected_right = True
                            else:
                                self.press_right = False
                                self.selected_right = False

                    fill_color_right = color.lighter_grey
                    fill_right = 0

            selected_color = color.forest_green
            if self.selected_up:
                fill_color_up = selected_color
                fill_up = 0
            if self.selected_down:
                fill_color_down = selected_color
                fill_down = 0
            if self.selected_left:
                fill_color_left = selected_color
                fill_left = 0
            if self.selected_right:
                fill_color_right = selected_color
                fill_right = 0

            pygame.draw.rect(surface, fill_color_up, up_box, fill_up)
            pygame.draw.rect(surface, fill_color_down, down_box, fill_down)
            pygame.draw.rect(surface, fill_color_left, left_box, fill_left)
            pygame.draw.rect(surface, fill_color_right, right_box, fill_right)

    class Point:
        y_adjust = margin * (1.5 * scaler)

        # 0 timer, 1 reaction time, 2 direction, -1 success/fail
        def __init__(self, point_data):
            self.time_marker = point_data[0]
            self.speed = point_data[1]
            self.direction = point_data[2]
            self.result = point_data[-1]  # False == Successful shot
            self.x = self.time_marker * graph.cols
            # self.y_adjust = margin * (1.5 * scaler)
            self.y = Point.y_adjust + (self.speed - fastest_time) * (
                    (surface_height - (margin * 3)) / (slowest_time - fastest_time))
            self.reaction_time = self.y
            self.color = [color.white, color.yellow, color.sky_blue, color.alert_red][self.direction - 1]
            self.radius = 5
            # self.ball = pygame.Rect((int(self.x), int(self.y)), (self.radius, self.radius))

        def get_point(self):
            return self.x, self.y

        def draw_point(self):

            if not (slowest_time - fastest_time):
                self.reaction_time = self.y_adjust + (self.reaction_time - fastest_time) * (
                        (surface_height - (margin * 3)) / 1)

            if box.press_up:
                if self.color == color.white:
                    pygame.draw.circle(surface, self.color, (self.x, self.reaction_time), self.radius, self.result)

            if box.press_down:
                if self.color == color.yellow:
                    pygame.draw.circle(surface, self.color, (self.x, self.reaction_time), self.radius, self.result)

            if box.press_left:
                if self.color == color.sky_blue:
                    pygame.draw.circle(surface, self.color, (self.x, self.reaction_time), self.radius, self.result)

            if box.press_right:
                if self.color == color.alert_red:
                    pygame.draw.circle(surface, self.color, (self.x, self.reaction_time), self.radius, self.result)

    def draw_line(data):

        for selector, direction in enumerate(data):
            line_color  = [color.white, color.yellow, color.sky_blue, color.alert_red][selector]
            activated   = [box.press_up, box.press_down, box.press_left, box.press_right][selector]

            for idx in range(len(direction)):

                if idx < len(direction) - 1 and activated:
                    start_x, start_y    = direction[idx][0] * graph.cols, \
                                          Point.y_adjust + (direction[idx][-1] - fastest_time) * \
                                          ((surface_height - (margin * 3)) / (slowest_time - fastest_time))

                    end_x, end_y        = direction[idx + 1][0] * graph.cols, \
                                          Point.y_adjust + (direction[idx + 1][-1] - fastest_time) * \
                                          ((surface_height - (margin * 3)) / (slowest_time - fastest_time))

                    pygame.draw.line(surface, line_color, (start_x, start_y), (end_x, end_y), 1)

    def summary(s_data, f_data):

        print(f"success data: {len(s_data)}\n{s_data}")
        print(f"fail data: {len(f_data)}\n{f_data}")

        up_times_success = [entry[2] for entry in s_data if entry[0] == 1]
        down_times_success = [entry[2] for entry in s_data if entry[0] == 2]
        left_times_success = [entry[2] for entry in s_data if entry[0] == 3]
        right_times_success = [entry[2] for entry in s_data if entry[0] == 4]

        up_times_fail = [entry[2] for entry in f_data if entry[0] == 1]
        down_times_fail = [entry[2] for entry in f_data if entry[0] == 2]
        left_times_fail = [entry[2] for entry in f_data if entry[0] == 3]
        right_times_fail = [entry[2] for entry in f_data if entry[0] == 4]

        up_succ_amount = len(up_times_success)
        down_succ_amount = len(down_times_success)
        left_succ_amount = len(left_times_success)
        right_succ_amount = len(right_times_success)

        up_fail_amount = len(up_times_fail)
        down_fail_amount = len(down_times_fail)
        left_fail_amount = len(left_times_fail)
        right_fail_amount = len(right_times_fail)

        up_total_amount = up_succ_amount + up_fail_amount
        down_total_amount = down_succ_amount + down_fail_amount
        left_total_amount = left_succ_amount + left_fail_amount
        right_total_amount = right_succ_amount + right_fail_amount

        # successful shot - reaction time averages
        up_times_success_average = sum(up_times_success) / up_succ_amount
        down_times_success_average = sum(down_times_success) / down_succ_amount
        left_times_success_average = sum(left_times_success) / left_succ_amount
        right_times_success_average = sum(right_times_success) / right_succ_amount

        # fail shot - reaction time averages

        up_times_fail_average = sum(up_times_fail) / up_fail_amount
        down_times_fail_average = sum(down_times_fail) / down_fail_amount
        left_times_fail_average = sum(left_times_fail) / left_fail_amount
        right_times_fail_average = sum(right_times_fail) / right_fail_amount

        all_times_success_averages = [up_times_success_average, down_times_success_average, left_times_success_average,
                                      right_times_success_average]

        all_times_fail_averages = [up_times_fail_average, down_times_fail_average, left_times_fail_average,
                                   right_times_fail_average]

        labels = ['up', 'down', 'left', 'right']

        # fastest success time by overall average
        fastest_average_time = min(all_times_success_averages)

        # slowest success time by overall average
        slowest_average_time = max(all_times_success_averages)

        # fastest success direction by overall average
        fastest_average_direction = labels[all_times_success_averages.index(fastest_average_time)]

        # slowest success direction by overall average
        slowest_average_direction = labels[all_times_success_averages.index(slowest_average_time)]

        # successful shot - percentage of total of shots
        up_shots_made_ptg = (up_succ_amount / up_total_amount) * 100
        down_shots_made_ptg = (down_succ_amount / down_total_amount) * 100
        left_shots_made_ptg = (left_succ_amount / left_total_amount) * 100
        right_shots_made_ptg = (right_succ_amount / right_total_amount) * 100

        # total percentage of successful shots
        all_shots_made_ptg = (sum([up_succ_amount, down_succ_amount, left_succ_amount, right_succ_amount]) / (
                len(s_data) + len(f_data))) * 100

        wrong_directions = [(entry[0], entry[1]) for entry in f_data if entry[0] != entry[1]]

        ########
        return (f"up_times_success_average:       {up_times_success_average}\n"
                f"down_times_success_average:     {down_times_success_average}\n"
                f"left_times_success_average:     {left_times_success_average}\n"
                f"right_times_success_average:    {right_times_success_average}\n"

                f"fastest_direction:              {fastest_average_direction} {fastest_average_time}\n"
                f"slowest_direction:              {slowest_average_direction} {slowest_average_time}\n"

                f"up_shots_made_ptg:              {round(up_shots_made_ptg, 2)}%\n"
                f"down_shots_made_ptg:            {round(down_shots_made_ptg, 2)}%\n"
                f"left_shots_made_ptg:            {round(left_shots_made_ptg, 2)}%\n"
                f"right_shots_made_ptg:           {round(right_shots_made_ptg, 2)}%\n"
                f"all_shots_made_ptg:             {round(all_shots_made_ptg, 2)}%")

    def draw_margin():
        pygame.draw.rect(surface, color.charcoal, (0, 0, surface_width, surface_height), margin)

    graph = Graph()
    box = Boxes()
    # 0 timer, 1 reaction time, 2 direction, -1 success/fail
    points = [Point([entry[0], entry[1], entry[2], entry[-1]]) for entry in all_data]

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    summary(success_data, fail_data)
                    return

        clock.tick(fps)
        surface.fill(color.black)
        mx, my = pygame.mouse.get_pos()

        graph.draw_graph()
        box.draw_box((mx, my))

        draw_margin()
        # render_text()
        #
        for point in points:
            point.draw_point()

        draw_line(line_data)





        pygame.display.update()
