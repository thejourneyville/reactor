import pygame
import reactor_colors as color
from statistics import multimode


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
    fast_slow_range = (slowest_time - fastest_time)
    if not fast_slow_range:
        fast_slow_range = 1

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

        def draw_legend_checkbox(self, mouse_cords, diff_x, diff_y):

            fill_color_up, fill_color_down, fill_color_left, fill_color_right = \
                color.cream, color.cream, color.cream, color.cream
            fill_up, fill_down, fill_left, fill_right = 1, 1, 1, 1

            up_box      = pygame.Rect(((diff_x + 40 * scaler), (diff_y + 12 * scaler), self.size, self.size))
            down_box    = pygame.Rect(((diff_x + 40 * scaler), (diff_y + 32 * scaler), self.size, self.size))
            left_box    = pygame.Rect(((diff_x + 40 * scaler), (diff_y + 52 * scaler), self.size, self.size))
            right_box   = pygame.Rect(((diff_x + 40 * scaler), (diff_y + 72 * scaler), self.size, self.size))

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

            pygame.draw.rect(surface, fill_color_up, up_box, fill_up)
            pygame.draw.rect(surface, fill_color_down, down_box, fill_down)
            pygame.draw.rect(surface, fill_color_left, left_box, fill_left)
            pygame.draw.rect(surface, fill_color_right, right_box, fill_right)

        def draw_stats_checkbox(self, mouse_cords, stats_diff_x, stats_diff_y):

            fill_color_stats = color.cream
            fill_stats = 1
            stats_box = pygame.Rect(stats_diff_x, stats_diff_y, self.stats_size, self.stats_size)

            x_mouse = mouse_cords[0]
            y_mouse = mouse_cords[-1]
            self.mouse_timer += 1

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
            if self.selected_stats:
                fill_color_stats = selected_color
                fill_stats = 0

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
                    (surface_height - (margin * 3)) / fast_slow_range)
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

            font_style_key = "/Users/thejourneyville/Documents/vscode/python/reactor/reactor/darkforest.ttf"
            coord_font = pygame.font.Font(f"{font_style_key}", int(15 * scaler))
            x_coord, y_coord = self.x, self.y + (30 * scaler)
            coord_surface = coord_font.render(f"{round(self.speed, 2)}", True, (255, 255, 255))
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
                                          ((surface_height - (margin * 3)) / fast_slow_range)

                    end_x, end_y        = direction[idx + 1][0] * graph.cols, \
                                          Point.y_adjust + (direction[idx + 1][-1] - fastest_time) * \
                                          ((surface_height - (margin * 3)) / fast_slow_range)

                    pygame.draw.line(surface, line_color, (start_x, start_y), (end_x, end_y), 1)

    def summary(s_data, f_data):

        labels = ['up', 'down', 'left', 'right']

        up_times_success = [entry[1] for entry in s_data if entry[2] == 1]
        down_times_success = [entry[1] for entry in s_data if entry[2] == 2]
        left_times_success = [entry[1] for entry in s_data if entry[2] == 3]
        right_times_success = [entry[1] for entry in s_data if entry[2] == 4]

        up_times_fail = [entry[1] for entry in f_data if entry[2] == 1]
        down_times_fail = [entry[1] for entry in f_data if entry[2] == 2]
        left_times_fail = [entry[1] for entry in f_data if entry[2] == 3]
        right_times_fail = [entry[1] for entry in f_data if entry[2] == 4]

        dir_succ = [up_times_success, down_times_success, left_times_success, right_times_success]
        dir_fail = [up_times_fail, down_times_fail, left_times_fail, right_times_fail]

        up_succ_amount = len(up_times_success)  # 0
        down_succ_amount = len(down_times_success)  # 0
        left_succ_amount = len(left_times_success)  # 0
        right_succ_amount = len(right_times_success)  # 1

        up_fail_amount = len(up_times_fail)  # 0
        down_fail_amount = len(down_times_fail)  # 0
        left_fail_amount = len(left_times_fail)  # 2
        right_fail_amount = len(right_times_fail)  # 8

        up_total_amount = up_succ_amount + up_fail_amount  # 0
        down_total_amount = down_succ_amount + down_fail_amount  # 0
        left_total_amount = left_succ_amount + left_fail_amount  # 2
        right_total_amount = right_succ_amount + right_fail_amount  # 9

        # successful shot - reaction time averages
        if up_succ_amount > 0:
            up_times_success_average = sum(up_times_success) / up_succ_amount  # 0.0e
        else:
            up_times_success_average = "NA"
        if down_succ_amount > 0:
            down_times_success_average = sum(down_times_success) / down_succ_amount  # 0.0e
        else:
            down_times_success_average = "NA"
        if left_succ_amount > 0:
            left_times_success_average = sum(left_times_success) / left_succ_amount  # 0.0e
        else:
            left_times_success_average = "NA"
        if right_succ_amount > 0:
            right_times_success_average = sum(right_times_success) / right_succ_amount  # 47.0
        else:
            right_times_success_average = "NA"

        all_succ_times = []
        for direction in dir_succ:
            for entry in direction:
                if entry:
                    all_succ_times.append(entry)
        if all_succ_times:
            all_times_success_average = sum(all_succ_times) / len(all_succ_times)
        else:
            all_times_success_average = "NA"

        # fail shot - reaction time averages
        if up_fail_amount > 0:
            up_times_fail_average = sum(up_times_fail) / up_fail_amount  # 0.0e
        else:
            up_times_fail_average = "NA"
        if down_fail_amount > 0:
            down_times_fail_average = sum(down_times_fail) / down_fail_amount  # 0.0e
        else:
            down_times_fail_average = "NA"
        if left_fail_amount > 0:
            left_times_fail_average = sum(left_times_fail) / left_fail_amount  # 1321.5
        else:
            left_times_fail_average = "NA"
        if right_fail_amount > 0:
            right_times_fail_average = sum(right_times_fail) / right_fail_amount  # 468.625
        else:
            right_times_fail_average = "NA"

        all_times_success_averages = [up_times_success_average, down_times_success_average, left_times_success_average,
                                      right_times_success_average]  # [0.0, 0.0, 0.0 47.0]
        all_times_success_averages = [item for item in all_times_success_averages if item != "NA"]

        all_times_fail_averages = [up_times_fail_average, down_times_fail_average, left_times_fail_average,
                                   right_times_fail_average]  # [0.0, 0.0, 1321.5, 468.625]

        # slowest success time by overall average and fastest success time by overall average
        if all_times_success_averages:
            slowest_average_time = max(all_times_success_averages)  # 47.0
            fastest = slowest_average_time  # 47.0
            for speed in all_times_success_averages:
                if fastest >= speed > 0:
                    fastest = speed
            fastest_average_time = fastest  # 47.0
        else:
            fastest_average_time = "NA"
            slowest_average_time = "NA"

        # fastest success direction by overall average
        if fastest_average_time == "NA":
            fastest_average_direction = "NA"
        else:
            fastest_average_direction = labels[all_times_success_averages.index(fastest_average_time)]  # right

        # slowest success direction by overall average
        if slowest_average_time == "NA":
            slowest_average_direction = "NA"
        else:
            slowest_average_direction = labels[all_times_success_averages.index(slowest_average_time)]  # right

        # successful shot - percentage of total of shots
        if up_succ_amount > 0:
            up_shots_made_ptg = (up_succ_amount / up_total_amount) * 100
        else:
            up_shots_made_ptg = "NA"
        if down_succ_amount > 0:
            down_shots_made_ptg = (down_succ_amount / down_total_amount) * 100
        else:
            down_shots_made_ptg = "NA"
        if left_succ_amount > 0:
            left_shots_made_ptg = (left_succ_amount / left_total_amount) * 100
        else:
            left_shots_made_ptg = "NA"
        if right_succ_amount > 0:
            right_shots_made_ptg = (right_succ_amount / right_total_amount) * 100
        else:
            right_shots_made_ptg = "NA"

        # total percentage of successful shots
        if sum([up_succ_amount, down_succ_amount, left_succ_amount, right_succ_amount]):
            all_shots_made_ptg = (sum([up_succ_amount, down_succ_amount, left_succ_amount, right_succ_amount]) / (
                    len(s_data) + len(f_data))) * 100
        else:
            all_shots_made_ptg = "NA"

        door_up, door_down, door_left, door_right = [], [], [], []
        all_wrong_directions = [(entry[0], entry[1]) for entry in current_react_data['fail'] if entry[0] != entry[1]]
        for item in all_wrong_directions:
            if item[-1] == 1:
                door_up.append(item)
            elif item[-1] == 2:
                door_down.append(item)
            elif item[-1] == 3:
                door_left.append(item)
            elif item[-1] == 4:
                door_right.append(item)
        all_wrong_doors_count = [len(door_up), len(door_down), len(door_left), len(door_right)]
        worst_wrong_door_count = max(all_wrong_doors_count)
        if worst_wrong_door_count == 0:
            worst_door_label = "NA"
        else:
            worst_door_index = all_wrong_doors_count.index(worst_wrong_door_count)
            worst_door_label = labels[worst_door_index]

        shot_up, shot_down, shot_left, shot_right = [], [], [], []
        for item in all_wrong_directions:
            if item[0] == 1:
                shot_up.append(item)
            elif item[0] == 2:
                shot_down.append(item)
            elif item[0] == 3:
                shot_left.append(item)
            elif item[0] == 4:
                shot_right.append(item)
        all_wrong_shots_count = [len(shot_up), len(shot_down), len(shot_left), len(shot_right)]
        worst_wrong_shots_count = max(all_wrong_shots_count)
        if worst_wrong_shots_count == 0:
            worst_shot_label = "NA"
        else:
            worst_shot_index = all_wrong_shots_count.index(worst_wrong_shots_count)
            worst_shot_label = labels[worst_shot_index]

        if all_wrong_directions:
            common_error = multimode(all_wrong_directions)
            # print(all_wrong_directions)
            # print(common_error)
            common_errors = [f"shot {labels[entry[0] - 1]} opened {labels[entry[-1] - 1]}" for entry in common_error]
            # common_error = f"shot {labels[common_error[0] - 1]} door opened {labels[common_error[-1] - 1]}"
            common_errors_len = len(common_errors)
        else:
            common_errors = None
            common_errors_len = 1

        # testing output
        # print(f"up_times_success_average:       {up_times_success_average}\n"
        #         f"down_times_success_average:     {down_times_success_average}\n"
        #         f"left_times_success_average:     {left_times_success_average}\n"
        #         f"right_times_success_average:    {right_times_success_average}\n"
        #         f"all_times_success_average:      {all_times_success_average}\n"
        #
        #         f"fastest_success_direction:      {fastest_average_direction}: {fastest_average_time}\n"
        #         f"slowest_success_direction:      {slowest_average_direction}: {slowest_average_time}\n"
        #
        #         f"up_shots_made_ptg:              {up_shots_made_ptg}%\n"
        #         f"down_shots_made_ptg:            {down_shots_made_ptg}%\n"
        #         f"left_shots_made_ptg:            {left_shots_made_ptg}%\n"
        #         f"right_shots_made_ptg:           {right_shots_made_ptg}%\n"
        #         f"all_shots_made_ptg:             {all_shots_made_ptg}%\n"
        #         f"worst wrong direction:          {worst_shot_label}: {worst_wrong_shots_count}\n"
        #         f"worst door accuracy:            {worst_door_label}: {worst_wrong_door_count}\n"
        #         f"most common wrong scenario:     {common_errors}")

        return (f"up times success average",
                f"{up_times_success_average}",
                f"down times success average",
                f"{down_times_success_average}",
                f"left times success average",
                f"{left_times_success_average}",
                f"right times success average",
                f"{right_times_success_average}",
                f"all_times_success_average",
                f"{all_times_success_average}",
                f"fastest success direction",
                f"{fastest_average_direction} {fastest_average_time}",
                f"slowest success direction",
                f"{slowest_average_direction} {slowest_average_time}",
                f"up shots made %",
                f"{up_shots_made_ptg}",
                f"down shots made %",
                f"{down_shots_made_ptg}",
                f"left shots made %",
                f"{left_shots_made_ptg}",
                f"right shots made %",
                f"{right_shots_made_ptg}",
                f"all shots made %",
                f"{all_shots_made_ptg}",
                f"worst wrong direction",
                f"{worst_shot_label} count {worst_wrong_shots_count}",
                f"worst door accuracy",
                f"{worst_door_label} count {worst_wrong_door_count}",
                f"most common wrong scenarios",
                common_errors), common_errors_len

    def render_summary(diff_x, diff_y, results):

        if box.selected_stats:
            font_style_key = "/Users/thejourneyville/Documents/vscode/python/reactor/reactor/Instruction.ttf"
            stats_font = pygame.font.Font(f"{font_style_key}", int(16 * scaler))
            stats_font_small = pygame.font.Font(f"{font_style_key}", int(8 * scaler))
            stats_color_label = (255, 112, 10)
            stats_color_data = (255, 137, 69)

            stat_positions = ((diff_x + 5 * scaler, (diff_y + 55 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 55 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 75 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 75 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 95 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 95 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 115 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 115 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 135 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 135 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 155 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 155 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 175 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 175 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 195 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 195 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 215 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 215 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 235 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 235 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 255 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 255 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 275 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 275 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 295 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 295 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 315 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 315 * scaler)),
                              (diff_x + 5 * scaler, (diff_y + 335 * scaler)),
                              (diff_x + 300 * scaler, (diff_y + 335 * scaler)))

            # this section preps the render to list all 'most common wrong scenarios'
            results_amend = results[:-1]
            stats_surfaces = [(stats_font.render(assignment, True, stats_color_label),
                               stat_positions[idx]) if idx % 2 == 0 else
                              (stats_font.render(assignment, True, stats_color_data),
                               stat_positions[idx])for idx, assignment in enumerate(results_amend)]

            if results[-1]:
                common_wrong_direction_entries = results[-1]
            else:
                common_wrong_direction_entries = ["NA"]

            output = [(diff_x + 300 * scaler, (diff_y + (335 + (20 * n)) * scaler))
                      for n in range(len(common_wrong_direction_entries))]

            wrong_direction_surfaces = [(stats_font.render(entry, True, stats_color_data), output[idx])
                                        for idx, entry in enumerate(common_wrong_direction_entries)]

            stats_surfaces += wrong_direction_surfaces
            stats_rects = [stats_surfaces[surf][0].get_rect() for surf in range(len(stats_surfaces))]

            for rect_idx in range(len(stats_rects)):
                stats_rects[rect_idx].bottomleft = stats_surfaces[rect_idx][-1]
                surface.blit(stats_surfaces[rect_idx][0], stats_rects[rect_idx])

    def draw_margin():
        pygame.draw.rect(surface, color.charcoal, (0, 0, surface_width, surface_height), margin)

    def render_legend_text(diff_x, diff_y):

        font_style_key = "/Users/thejourneyville/Documents/vscode/python/reactor/reactor/darkforest.ttf"

        key_font = pygame.font.Font(f"{font_style_key}", int(15 * scaler))

        labels = ["UP", "DOWN", "LEFT", "RIGHT"]

        box_colors = color.stats

        key_positions = ((diff_x + 5 * scaler, (diff_y + 25 * scaler)),
                         (diff_x + 5 * scaler, (diff_y + 45 * scaler)),
                         (diff_x + 5 * scaler, (diff_y + 65 * scaler)),
                         (diff_x + 5 * scaler, (diff_y + 85 * scaler)))

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

    def move_legend(m_x, m_y, xdiff, ydiff):

        background_color = color.black
        outline_color = color.lightgrey

        pygame.draw.rect(surface, background_color, ((m_x - xdiff, m_y - ydiff), (x_legend_size, y_legend_size)))
        pygame.draw.rect(surface, outline_color, ((m_x - xdiff, m_y - ydiff), (x_legend_size, y_legend_size)), 1)

        return m_x - xdiff, m_y - ydiff

    def draw_stats(m_x, m_y, yadd):

        background_color = color.black
        outline_color = color.lightgrey

        if box.selected_stats:
            pygame.draw.rect(surface, background_color, ((m_x, m_y), (x_stats_size, y_stats_size + (yadd * 20))))
            pygame.draw.rect(surface, outline_color, ((m_x, m_y), (x_stats_size, y_stats_size + (yadd * 20))), 1)
        else:
            pygame.draw.rect(surface, background_color, ((m_x, m_y), (x_stats_size, box.stats_size)))
            pygame.draw.rect(surface, outline_color, ((m_x, m_y), (x_stats_size, box.stats_size)), 1)

    def move_stats(m_x, m_y, xdiff, ydiff, yadd):

        background_color = color.black
        outline_color = color.lightgrey

        if box.selected_stats:
            pygame.draw.rect(surface, background_color, ((m_x - xdiff, m_y - ydiff), (x_stats_size, y_stats_size + (yadd * 20))))
            pygame.draw.rect(surface, outline_color, ((m_x - xdiff, m_y - ydiff), (x_stats_size, y_stats_size + (yadd * 20))), 1)
        else:
            pygame.draw.rect(surface, background_color, ((m_x - xdiff, m_y - ydiff), (x_stats_size, box.stats_size)))
            pygame.draw.rect(surface, outline_color, ((m_x - xdiff, m_y - ydiff), (x_stats_size, box.stats_size)), 1)

        return m_x - xdiff, m_y - ydiff

    # LEGEND WINDOW
    def menu_order_0(last, measured, x_pos, y_pos, s_x_pos, s_y_pos, xdiff, ydiff):
        if not box.stats_moving:
            if all([x_pos - 5 <= mx <= x_pos + x_legend_size + 5,
                    y_pos - 5 <= my <= y_pos + y_legend_size + 5]):

                if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                    box.legend_moving = True
                    last = 0

                    if not measured:
                        xdiff = abs(mx - x_pos)
                        ydiff = abs(my - y_pos)
                        measured = True

                    draw_stats(stats_x_pos, stats_y_pos, y_add)
                    box.draw_stats_checkbox((mx, my), s_x_pos, s_y_pos)
                    render_summary(s_x_pos, s_y_pos, stat_results)
                    x_pos, y_pos = move_legend(mx, my, xdiff, ydiff)
                    render_legend_text(x_pos, y_pos)
                    box.draw_legend_checkbox((mx, my), x_pos, y_pos)

                else:
                    box.legend_moving = False
                    measured = False
                    draw_legend(x_pos, y_pos)
                    render_legend_text(x_pos, y_pos)
                    box.draw_legend_checkbox((mx, my), x_pos, y_pos)
                    draw_stats(s_x_pos, s_y_pos, y_add)
                    box.draw_stats_checkbox((mx, my), s_x_pos, s_y_pos)
                    render_summary(s_x_pos, s_y_pos, stat_results)

            else:
                draw_legend(x_pos, y_pos)
                render_legend_text(x_pos, y_pos)
                box.draw_legend_checkbox((mx, my), x_pos, y_pos)
                draw_stats(stats_x_pos, s_y_pos, y_add)
                box.draw_stats_checkbox((mx, my), s_x_pos, s_y_pos)
                render_summary(s_x_pos, s_y_pos, stat_results)

        return last, measured, x_pos, y_pos, xdiff, ydiff

    # STATS WINDOW
    def menu_order_1(last, measured, x_pos, y_pos, l_x_pos, l_y_pos, xdiff, ydiff):
        if not box.legend_moving:
            if any([box.selected_stats and all([x_pos - 5 <= mx <= x_pos + x_stats_size + 5,
                                                y_pos - 5 <= my <= y_pos + y_stats_size + 5]),
                    not box.selected_stats and all([x_pos - 5 <= mx <= x_pos + x_stats_size + 5,
                                                    y_pos - 5 <= my <= y_pos + box.stats_size + 5])]):

                if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                    box.stats_moving = True
                    last = 1

                    if not measured:  # locks mouse position relative to top-left corner of box until release
                        xdiff = abs(mx - x_pos)
                        ydiff = abs(my - y_pos)
                        measured = True

                    draw_legend(l_x_pos, l_y_pos)
                    render_legend_text(l_x_pos, l_y_pos)
                    box.draw_legend_checkbox((mx, my), l_x_pos, l_y_pos)
                    x_pos, y_pos = move_stats(mx, my, xdiff, ydiff, y_add)
                    render_summary(x_pos, y_pos, stat_results)
                    box.draw_stats_checkbox((mx, my), x_pos, y_pos)
                    # draw_stats(x_pos, y_pos, y_add)

                else:
                    box.stats_moving = False
                    measured = False
                    draw_stats(x_pos, y_pos, y_add)
                    box.draw_stats_checkbox((mx, my), x_pos, y_pos)
                    render_summary(x_pos, y_pos, stat_results)
                    draw_legend(l_x_pos, l_y_pos)
                    render_legend_text(l_x_pos, l_y_pos)
                    box.draw_legend_checkbox((mx, my), l_x_pos, l_y_pos)

            else:
                draw_stats(x_pos, y_pos, y_add)
                box.draw_stats_checkbox((mx, my), x_pos, y_pos)
                render_summary(x_pos, y_pos, stat_results)
                draw_legend(l_x_pos, l_y_pos)
                render_legend_text(l_x_pos, l_y_pos)
                box.draw_legend_checkbox((mx, my), l_x_pos, l_y_pos)

        return last, measured, x_pos, y_pos, xdiff, ydiff

    graph = Graph()
    box = Boxes()
    # success_data = [(entry[-1], entry[2], entry[0], False) for entry in current_react_data['success']]
    # 0 timer, 1 reaction time, 2 direction, -1 success/fail
    points = [Point([entry[0], entry[1], entry[2], entry[-1]]) for entry in all_data]

    stat_results, y_add = summary(success_data, fail_data)

    # moving menu variables
    x_legend_size = 60 * scaler
    y_legend_size = 90 * scaler
    legend_x_pos = margin
    legend_y_pos = margin
    x_stats_size = 585 * scaler
    y_stats_size = 345 * scaler
    stats_x_pos = surface_width - (margin + 585 * scaler)
    stats_y_pos = margin
    mouse_measurement = False
    last_menu = 0
    x_diff, y_diff = 0, 0

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # summary(success_data, fail_data)
                    return stat_results

        clock.tick(fps)
        surface.fill(color.black)
        mx, my = pygame.mouse.get_pos()

        graph.draw_graph()
        draw_margin()

        for point in points:
            point.draw_point()
            point.draw_coords()
        draw_line(line_data)

        if last_menu == 0:
            last_menu, mouse_measurement, legend_x_pos, legend_y_pos, x_diff, y_diff = \
                menu_order_0(last_menu, mouse_measurement, legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos, x_diff, y_diff)
            last_menu, mouse_measurement, stats_x_pos, stats_y_pos, x_diff, y_diff = \
                menu_order_1(last_menu, mouse_measurement, stats_x_pos, stats_y_pos, legend_x_pos, legend_y_pos, x_diff, y_diff)

        if last_menu == 1:
            last_menu, mouse_measurement, stats_x_pos, stats_y_pos, x_diff, y_diff = \
                menu_order_1(last_menu, mouse_measurement, stats_x_pos, stats_y_pos, legend_x_pos, legend_y_pos, x_diff, y_diff)
            last_menu, mouse_measurement, legend_x_pos, legend_y_pos, x_diff, y_diff = \
                menu_order_0(last_menu, mouse_measurement, legend_x_pos, legend_y_pos, stats_x_pos, stats_y_pos, x_diff, y_diff)

        pygame.display.flip()

