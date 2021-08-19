import pygame
import colors
import reactor_colors as color


def stats(surface, surface_width, surface_height, margin_color, scaler, clock, fps, level, current_react_data,
          time_elapsed):
    pygame.display.set_caption(f"PLAYER STATISTICS")
    margin = int(30 * scaler)

    if not current_react_data:
        return

    success_data    = [(entry[-1], entry[2], entry[0], False) for entry in current_react_data['success']]
    fail_data       = [(entry[-1], entry[2], entry[0], True) for entry in current_react_data['fail']]
    all_data        = sorted((success_data + fail_data), key=lambda x: x[0])  # sorted by time elapsed

    up_data     = [(entry[0], entry[1]) for entry in all_data if entry[2] == 1]
    down_data   = [(entry[0], entry[1]) for entry in all_data if entry[2] == 2]
    left_data   = [(entry[0], entry[1]) for entry in all_data if entry[2] == 3]
    right_data  = [(entry[0], entry[1]) for entry in all_data if entry[2] == 4]
    line_data   = [up_data, down_data, left_data, right_data]

    slowest_time = max([idx[1] for idx in all_data])
    fastest_time = min([idx[1] for idx in all_data])

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
            self.size = 10 * scaler
            self.stats_size = 20 * scaler
            self.mouse_timer = 0
            self.selected_up = True
            self.selected_down = True
            self.selected_left = True
            self.selected_right = True
            self.legend_moving = False
            self.selected_stats = False
            self.stats_moving = False

        def draw_checkbox(self, mouse_cords, diff_x, diff_y, stats_diff_x, stats_diff_y):

            fill_color_up, fill_color_down, fill_color_left, fill_color_right, fill_color_stats = \
                color.cream, color.cream, color.cream, color.cream, color.cream
            fill_up, fill_down, fill_left, fill_right, fill_stats = 1, 1, 1, 1, 1

            up_box      = pygame.Rect(((diff_x + 40 * scaler), (diff_y + 12 * scaler), self.size, self.size))
            down_box    = pygame.Rect(((diff_x + 40 * scaler), (diff_y + 32 * scaler), self.size, self.size))
            left_box    = pygame.Rect(((diff_x + 40 * scaler), (diff_y + 52 * scaler), self.size, self.size))
            right_box   = pygame.Rect(((diff_x + 40 * scaler), (diff_y + 72 * scaler), self.size, self.size))
            stats_box   = pygame.Rect(stats_diff_x, stats_diff_y, self.stats_size, self.stats_size)

            x_mouse = mouse_cords[0]
            y_mouse = mouse_cords[-1]
            self.mouse_timer += 1

            if not self.stats_moving:
                if up_box.left <= x_mouse <= (up_box.left + self.size):
                    if up_box.top <= y_mouse <= (up_box.top + self.size):

                        if self.mouse_timer >= 20:
                            if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                                if not self.selected_up:
                                    self.selected_up = True
                                else:
                                    self.selected_up = False
                                self.mouse_timer = 0

                        fill_color_up = color.lighter_grey
                        fill_up = 0

                if down_box.left <= x_mouse <= (down_box.left + self.size):
                    if down_box.top <= y_mouse <= (down_box.top + self.size):

                        if self.mouse_timer >= 20:
                            if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                                if not self.selected_down:
                                    self.selected_down = True
                                else:
                                    self.selected_down = False
                                self.mouse_timer = 0

                        fill_color_down = color.lighter_grey
                        fill_down = 0

                if left_box.left <= x_mouse <= (left_box.left + self.size):
                    if left_box.top <= y_mouse <= (left_box.top + self.size):

                        if self.mouse_timer >= 20:
                            if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                                if not self.selected_left:
                                    self.selected_left = True
                                else:
                                    self.selected_left = False
                                self.mouse_timer = 0

                        fill_color_left = color.lighter_grey
                        fill_left = 0

                if right_box.left <= x_mouse <= (right_box.left + self.size):
                    if right_box.top <= y_mouse <= (right_box.top + self.size):

                        if self.mouse_timer >= 20:
                            if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                                if not self.selected_right:
                                    self.selected_right = True
                                else:
                                    self.selected_right = False
                                self.mouse_timer = 0

                        fill_color_right = color.lighter_grey
                        fill_right = 0

            if not self.legend_moving:
                if stats_box.left <= x_mouse <= (stats_box.left + self.stats_size):
                    if stats_box.top <= y_mouse <= (stats_box.top + self.stats_size):

                        if self.mouse_timer >= 20:
                            if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                                if not self.selected_stats:
                                    self.selected_stats = True
                                else:
                                    self.selected_stats = False
                                self.mouse_timer = 0

                        fill_color_stats = color.lighter_grey
                        fill_stats = 0

            selected_color = color.cream
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
            if self.selected_stats:
                fill_color_stats = selected_color
                fill_stats = 0

            pygame.draw.rect(surface, fill_color_up, up_box, fill_up)
            pygame.draw.rect(surface, fill_color_down, down_box, fill_down)
            pygame.draw.rect(surface, fill_color_left, left_box, fill_left)
            pygame.draw.rect(surface, fill_color_right, right_box, fill_right)
            pygame.draw.rect(surface, fill_color_stats, stats_box, fill_stats)

    class Point:
        y_adjust = margin * (1.5 * scaler)

        def __init__(self, point_data):
            self.time_marker = point_data[0]
            self.speed = point_data[1]
            self.direction = point_data[2]
            self.result = point_data[-1]  # False == Successful shot because 0 represents solid fill on circle
            self.x = self.time_marker * graph.cols
            self.y = Point.y_adjust + (self.speed - fastest_time) * (
                    (surface_height - (margin * 3)) / (slowest_time - fastest_time))
            self.reaction_time = self.y
            self.color = color.stats[self.direction - 1]
            self.radius = 10 * scaler

        def get_point(self):
            return self.x, self.y

        def draw_point(self):

            if not (slowest_time - fastest_time):
                self.reaction_time = self.y_adjust + (self.reaction_time - fastest_time) * (
                        (surface_height - (margin * 3)) / 1)

            if box.selected_up:
                if self.direction - 1 == 0:
                    pygame.draw.circle(surface, self.color, (self.x, self.reaction_time), self.radius, self.result)

            if box.selected_down:
                if self.direction - 1 == 1:
                    pygame.draw.circle(surface, self.color, (self.x, self.reaction_time), self.radius, self.result)

            if box.selected_left:
                if self.direction - 1 == 2:
                    pygame.draw.circle(surface, self.color, (self.x, self.reaction_time), self.radius, self.result)

            if box.selected_right:
                if self.direction - 1 == 3:
                    pygame.draw.circle(surface, self.color, (self.x, self.reaction_time), self.radius, self.result)

        def draw_coords(self):

            font_style_key = "darkforest.ttf"
            coord_font = pygame.font.Font(f"./{font_style_key}", int(15 * scaler))
            x_coord, y_coord = self.x, self.y + (30 * scaler)
            coord_surface = coord_font.render(f"{round(self.speed, 2)}", True, colors.WHITE)
            coord_rect = coord_surface.get_rect()
            coord_rect.bottomleft = (x_coord, y_coord)

            if box.selected_up:
                if self.direction == 1:
                    surface.blit(coord_surface, coord_rect)

            if box.selected_down:
                if self.direction == 2:
                    surface.blit(coord_surface, coord_rect)

            if box.selected_left:
                if self.direction == 3:
                    surface.blit(coord_surface, coord_rect)

            if box.selected_right:
                if self.direction == 4:
                    surface.blit(coord_surface, coord_rect)

    def draw_line(data):

        for selector, direction in enumerate(data):
            line_color  = color.stats[selector]
            activated   = [box.selected_up, box.selected_down, box.selected_left, box.selected_right][selector]

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

        # print(f"success data: {len(s_data)}\n{s_data}")
        # print(f"fail data: {len(f_data)}\n{f_data}")

        up_times_success = [entry[1] for entry in s_data if entry[2] == 1]
        down_times_success = [entry[1] for entry in s_data if entry[2] == 2]
        left_times_success = [entry[1] for entry in s_data if entry[2] == 3]
        right_times_success = [entry[1] for entry in s_data if entry[2] == 4]

        up_times_fail = [entry[1] for entry in f_data if entry[2] == 1]
        down_times_fail = [entry[1] for entry in f_data if entry[2] == 2]
        left_times_fail = [entry[1] for entry in f_data if entry[2] == 3]
        right_times_fail = [entry[1] for entry in f_data if entry[2] == 4]

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

        # wrong_directions = [(entry[0], entry[1]) for entry in f_data if entry[0] != entry[1]]

        ########
        return (f"up_times_success_average:       {up_times_success_average}\n"
                f"down_times_success_average:     {down_times_success_average}\n"
                f"left_times_success_average:     {left_times_success_average}\n"
                f"right_times_success_average:    {right_times_success_average}\n"

                f"fastest_success_direction:      {fastest_average_direction} {fastest_average_time}\n"
                f"slowest_success_direction:      {slowest_average_direction} {slowest_average_time}\n"

                f"up_shots_made_ptg:              {round(up_shots_made_ptg, 2)}%\n"
                f"down_shots_made_ptg:            {round(down_shots_made_ptg, 2)}%\n"
                f"left_shots_made_ptg:            {round(left_shots_made_ptg, 2)}%\n"
                f"right_shots_made_ptg:           {round(right_shots_made_ptg, 2)}%\n"
                f"all_shots_made_ptg:             {round(all_shots_made_ptg, 2)}%")

    def draw_margin():
        pygame.draw.rect(surface, color.charcoal, (0, 0, surface_width, surface_height), margin)

    def render_legend_text(diff_x, diff_y):

        font_style_key = "darkforest.ttf"

        key_font = pygame.font.Font(f"./{font_style_key}", int(15 * scaler))

        labels = ["UP", "DOWN", "LEFT", "RIGHT"]

        box_colors = color.stats

        key_positions = [(diff_x + 5 * scaler, (diff_y + 25 * scaler)),
                         (diff_x + 5 * scaler, (diff_y + 45 * scaler)),
                         (diff_x + 5 * scaler, (diff_y + 65 * scaler)),
                         (diff_x + 5 * scaler, (diff_y + 85 * scaler))]

        key_surfaces = [(key_font.render(f"{labels[assignment]}",
                        True, box_colors[assignment]),
                        key_positions[assignment]) for assignment in range(len(key_positions))]

        key_rects = [key_surfaces[surf][0].get_rect() for surf in range(len(key_surfaces))]

        for rect_idx in range(len(key_rects)):
            key_rects[rect_idx].bottomleft = key_surfaces[rect_idx][-1]
            surface.blit(key_surfaces[rect_idx][0], key_rects[rect_idx])

    def draw_legend(m_x, m_y):

        background_color = color.black
        outline_color = color.lightgrey

        pygame.draw.rect(surface, background_color, ((m_x, m_y), (x_legend_size, y_legend_size)))
        pygame.draw.rect(surface, outline_color, ((m_x, m_y), (x_legend_size, y_legend_size)), 1)

    def move_legend(m_x, m_y):

        background_color = color.black
        outline_color = color.lightgrey

        pygame.draw.rect(surface, background_color, ((m_x - x_diff, m_y - y_diff), (x_legend_size, y_legend_size)))
        pygame.draw.rect(surface, outline_color, ((m_x - x_diff, m_y - y_diff), (x_legend_size, y_legend_size)), 1)

        return m_x - x_diff, m_y - y_diff

    def draw_stats(m_x, m_y):

        background_color = color.black
        outline_color = color.lightgrey

        if box.selected_stats:
            pygame.draw.rect(surface, background_color, ((m_x, m_y), (x_stats_size, y_stats_size)))
            pygame.draw.rect(surface, outline_color, ((m_x, m_y), (x_stats_size, y_stats_size)), 1)
        else:
            pygame.draw.rect(surface, background_color, ((m_x, m_y), (x_stats_size, box.stats_size)))
            pygame.draw.rect(surface, outline_color, ((m_x, m_y), (x_stats_size, box.stats_size)), 1)

    def move_stats(m_x, m_y):

        background_color = color.black
        outline_color = color.lightgrey

        if box.selected_stats:
            pygame.draw.rect(surface, background_color, ((m_x - x_diff, m_y - y_diff), (x_stats_size, y_stats_size)))
            pygame.draw.rect(surface, outline_color, ((m_x - x_diff, m_y - y_diff), (x_stats_size, y_stats_size)), 1)
        else:
            pygame.draw.rect(surface, background_color, ((m_x - x_diff, m_y - y_diff), (x_stats_size, box.stats_size)))
            pygame.draw.rect(surface, outline_color, ((m_x - x_diff, m_y - y_diff), (x_stats_size, box.stats_size)), 1)

        return m_x - x_diff, m_y - y_diff

    graph = Graph()
    box = Boxes()
    # success_data = [(entry[-1], entry[2], entry[0], False) for entry in current_react_data['success']]
    # 0 timer, 1 reaction time, 2 direction, -1 success/fail
    points = [Point([entry[0], entry[1], entry[2], entry[-1]]) for entry in all_data]

    # print(summary(success_data, fail_data))
    x_legend_size = 60 * scaler
    y_legend_size = 90 * scaler
    legend_x_pos = margin
    legend_y_pos = margin
    legend_measured = False

    x_stats_size = 240 * scaler
    y_stats_size = 360 * scaler
    stats_x_pos = margin
    stats_y_pos = (surface_height - (margin + y_stats_size))
    stats_measured = False

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
        draw_margin()

        for point in points:
            point.draw_point()
            point.draw_coords()
        draw_line(line_data)

        if not box.stats_moving:
            if all([legend_x_pos - 5 <= mx <= legend_x_pos + x_legend_size + 5,
                    legend_y_pos - 5 <= my <= legend_y_pos + y_legend_size + 5]):

                if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                    box.legend_moving = True
                    if not legend_measured:
                        x_diff = abs(mx - legend_x_pos)
                        y_diff = abs(my - legend_y_pos)
                        legend_measured = True
                    box.draw_checkbox((mx, my), legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos)
                    legend_x_pos, legend_y_pos = move_legend(mx, my)
                    render_legend_text(legend_x_pos, legend_y_pos)

                else:
                    box.legend_moving = False
                    legend_measured = False
                    box.draw_checkbox((mx, my), legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos)
                    draw_legend(legend_x_pos, legend_y_pos)
                    render_legend_text(legend_x_pos, legend_y_pos)

            else:
                box.draw_checkbox((mx, my), legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos)
                draw_legend(legend_x_pos, legend_y_pos)
                render_legend_text(legend_x_pos, legend_y_pos)

        else:
            draw_legend(legend_x_pos, legend_y_pos)
            render_legend_text(legend_x_pos, legend_y_pos)
            box.draw_checkbox((mx, my), legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos)

        if not box.legend_moving:
            if any([box.selected_stats and all([stats_x_pos - 5 <= mx <= stats_x_pos + x_stats_size + 5,
                    stats_y_pos - 5 <= my <= stats_y_pos + y_stats_size + 5]),
                    not box.selected_stats and all([stats_x_pos - 5 <= mx <= stats_x_pos + x_stats_size + 5,
                    stats_y_pos - 5 <= my <= stats_y_pos + box.stats_size + 5])]):

                if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                    box.stats_moving = True
                    if not stats_measured:
                        x_diff = abs(mx - stats_x_pos)
                        y_diff = abs(my - stats_y_pos)
                        stats_measured = True
                    stats_x_pos, stats_y_pos = move_stats(mx, my)
                    box.draw_checkbox((mx, my), legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos)
                    # render_stats_text(legend_x_pos, legend_y_pos)

                else:
                    box.stats_moving = False
                    stats_measured = False
                    draw_stats(stats_x_pos, stats_y_pos)
                    box.draw_checkbox((mx, my), legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos)
                    # render_stats_text(stats_x_pos, stats_y_pos)

            else:
                draw_stats(stats_x_pos, stats_y_pos)
                box.draw_checkbox((mx, my), legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos)
                # render_stats_text(legend_x_pos, legend_y_pos)
        else:
            draw_stats(stats_x_pos, stats_y_pos)
            box.draw_checkbox((mx, my), legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos)
            # render_stats_text(legend_x_pos, legend_y_pos)

        pygame.display.flip()