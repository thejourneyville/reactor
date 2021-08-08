import pygame
import reactor_colors as color


def stats(surface, surface_width, surface_height, margin_color,
          scaler, clock, fps, level, current_react_data, time_elapsed):

    pygame.display.set_caption(f"PLAYER STATISTICS")
    margin = int(30 * scaler)

    data = current_react_data
    door_speed = data['door_speed']
    disc_speed = data['disc_speed']
    disc_size = data['disc_size']
    success = data['success']
    fail = data['fail']
    entries, successes, fails = (len(success) + len(fail)), len(success), len(fail)
    all_entries = (success + fail)
    success_directions = [entry[0] for entry in success]
    fail_directions = [entry[1] for entry in fail]
    success_times = [entry[2] for entry in success]
    fail_times = [entry[2] for entry in fail]
    all_times = success_times + fail_times
    slowest_time = max(all_times)
    fastest_time = min(all_times)
    print(f"current surface height minus margins * 2: {surface_height - (margin * 2)}")

    successes = [entry for entry in current_react_data['success']]
    fails = [entry for entry in current_react_data['fail']]
    all_shot_entries = successes + fails

    up = [(entry[-1], entry[2])
          for entry in sorted([entry for entry in all_shot_entries if entry[0] == 1], key=lambda x: x[-1])]
    down = [(entry[-1], entry[2])
            for entry in sorted([entry for entry in all_shot_entries if entry[0] == 2], key=lambda x: x[-1])]
    left = [(entry[-1], entry[2])
            for entry in sorted([entry for entry in all_shot_entries if entry[0] == 3], key=lambda x: x[-1])]
    right = [(entry[-1], entry[2])
             for entry in sorted([entry for entry in all_shot_entries if entry[0] == 4], key=lambda x: x[-1])]

    entries_directions = [up, down, left, right]
    # for direction in entries_directions:
    #     for entry in direction:
    #         print(entry)

    if success_times:
        fastest_success = min(success_times)
    else:
        fastest_success = min(fail_times)
    if fail_times:
        slowest_fail = max(fail_times)
    else:
        slowest_fail = max(success_times)
    time_stamp_success = [entry[-1] for entry in success]
    time_stamp_fail = [entry[-1] for entry in fail]
    time_stamp_total = (time_stamp_success + time_stamp_fail)
    time_stamp_total = sorted(time_stamp_total)

    # print(f"stats screen: {level}")
    # print("stats screen: current_react_data:")
    # print(f"door speed: {data['door_speed']}")
    # print(f"total entries, successes, fails: {entries, successes, fails}")
    # print(f"success directions: {success_directions}")
    # print(f"fail_directions: {fail_directions}")
    # print(f"success_times: {success_times}")
    # print(f"fail times: {fail_times}")
    # print(f"time stamp total: {time_stamp_total}")

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
            # self.true_point_radius = 10
            # self.point_radius = self.true_point_radius * scaler
            # self.point_up = pygame.Rect((self.x, self.y), (self.point_radius * 2, self.point_radius * 2))
            # print(self.height)

        def draw_graph(self):
            for row in range(self.row_amount):
                # rows
                pygame.draw.line(surface,
                                 self.gridline_color,
                                 (0, int(self.y_adjust + (self.rows * row))),
                                 (surface_width, int(self.y_adjust + (self.rows * row))),
                                 self.gridline_width)

            for col in range(int(self.cols_amount)):
                # cols
                pygame.draw.line(surface,
                                 self.gridline_color,
                                 (int(self.y_adjust + (self.cols * col)), 0),
                                 (int(self.y_adjust + (self.cols * col)), surface_height),
                                 self.gridline_width)

    class Point:
        def __init__(self, p):
            self.time_marker = p[0]
            self.reaction_time = p[1]
            self.result = p[-1]
            self.x = self.time_marker * graph.cols
            self.y_adjust = margin * 1.5
            self.y = self.y_adjust + (self.reaction_time - fastest_time) * ((surface_height - (margin * 3)) / (slowest_time - fastest_time))
            self.reaction_time = self.y
            self.color = [color.white, color.yellow, color.sky_blue, color.alert_red][p[2] - 1]
            self.radius = 5
            self.ball = pygame.Rect((int(self.x), int(self.y)), (self.radius, self.radius))

        def draw_point(self):

            if not (slowest_time - fastest_time):
                self.reaction_time = self.y_adjust + (self.reaction_time - fastest_time) * (
                            (surface_height - (margin * 3)) / 1)

            if box.press_up:
                if self.color == color.white:
                    pygame.draw.circle(
                        surface,
                        self.color,
                        (self.x, self.reaction_time),
                        self.radius,
                        self.result)

            if box.press_down:
                if self.color == color.yellow:
                    pygame.draw.circle(
                        surface,
                        self.color,
                        (self.x, self.reaction_time),
                        self.radius,
                        self.result)

            if box.press_left:
                if self.color == color.sky_blue:
                    pygame.draw.circle(
                        surface,
                        self.color,
                        (self.x, self.reaction_time),
                        self.radius,
                        self.result)

            if box.press_right:
                if self.color == color.alert_red:
                    pygame.draw.circle(
                        surface,
                        self.color,
                        (self.x, self.reaction_time),
                        self.radius,
                        self.result)

    class Boxes:
        def __init__(self):
            self.size_x = 10
            self.size_y = 10
            self.selected = True
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

            up_box = pygame.Rect((margin + 35, margin - 7, self.size_x, self.size_y))
            down_box = pygame.Rect((margin + 35, margin + 13, self.size_x, self.size_y))
            left_box = pygame.Rect((margin + 35, margin + 33, self.size_x, self.size_y))
            right_box = pygame.Rect((margin + 35, margin + 53, self.size_x, self.size_y))

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

    def draw_line(directions):

        for idx, direction in enumerate(directions):

            selected_state = [box.press_up, box.press_down, box.press_left, box.press_right][idx]
            line_color = [color.white, color.yellow, color.sky_blue, color.alert_red][idx]

            if not (slowest_time - fastest_time):
                reaction_time_range = 1
            else:
                reaction_time_range = (slowest_time - fastest_time)

            if selected_state:
                for entry_idx, entry in enumerate(direction):

                    if entry_idx < len(direction) - 1:
                        x_start, y_start = entry[0], entry[-1]
                        x_end, y_end = direction[entry_idx + 1][0], direction[entry_idx + 1][-1]

                        y_start = point.y_adjust + \
                                  (y_start - fastest_time) * \
                                  ((surface_height - (margin * 3)) / reaction_time_range)
                        y_end = point.y_adjust + \
                                (y_end - fastest_time) * \
                                ((surface_height - (margin * 3)) / reaction_time_range)

                        pygame.draw.line(surface,
                                         line_color,
                                         (x_start * graph.cols, y_start),
                                         (x_end * graph.cols, y_end),
                                         1)

    def draw_margin():
        pygame.draw.rect(surface, color.charcoal, (0, 0, surface_width, surface_height), margin)

    def render_text():

        font_style_key = "darkforest.ttf"

        key_font = pygame.font.Font(f"./{font_style_key}", int(15 * scaler))

        labels = ["UP", "DOWN", "LEFT", "RIGHT"]
        colors = [color.white, color.yellow, color.sky_blue, color.alert_red]
        positions = [(margin, margin + 5),
                     (margin, margin + 25),
                     (margin, margin + 45),
                     (margin, margin + 65)]

        surfaces = []
        for direction in range(4):
            surfaces.append((key_font.render(f"{labels[direction]}", True, colors[direction]), positions[direction]))

        rects = []
        for surf in range(4):
            rects.append(surfaces[surf][0].get_rect())

        for placement in range(4):
            rects[placement].bottomleft = surfaces[placement][-1]
            surface.blit(surfaces[placement][0], rects[placement])

        coord_pos = []
        for coord in all_points:
            coord_pos.append((coord.x, coord.y))

        surfaces = []
        for idx, direction in enumerate(coord_pos):
            surfaces.append(((key_font.render(f"{all_entries[idx][2]}", True, color.white)), direction))

        rects = []
        for surf in surfaces:
            rects.append(surf[0].get_rect())

        for idx, placement in enumerate(rects):
            placement.bottomleft = (surfaces[idx][-1][0], surfaces[idx][-1][-1] + (30 * scaler))
            if all_entries[idx][0] == 1 and box.selected_up:
                surface.blit(surfaces[idx][0], placement)
            if all_entries[idx][0] == 2 and box.selected_down:
                surface.blit(surfaces[idx][0], placement)
            if all_entries[idx][0] == 3 and box.selected_left:
                surface.blit(surfaces[idx][0], placement)
            if all_entries[idx][0] == 4 and box.selected_right:
                surface.blit(surfaces[idx][0], placement)

        # for reference
        # level_font_surface = level_font.render(f"LEVEL {level}", True, color.instructions_color)
        # instructions_surface = instructions_font.render(
        #     f"must score {score_goal} points in {time_limit} seconds", True, color.instructions_color)
        # speed_font_surface = speed_font.render(f"reactor speed {door_speed}", True, color.alert_red)
        #
        # level_font_rect = level_font_surface.get_rect()
        # instructions_rect = instructions_surface.get_rect()
        # speed_font_rect = speed_font_surface.get_rect()
        #
        # level_font_rect.centerx, level_font_rect.centery = level_font_position, surface_height // 2 - (30 * scaler)
        # instructions_rect.centerx, instructions_rect.centery = surface_width // 2, surface_height // 2 + (60 * scaler)
        # speed_font_rect.center = (surface_width // 2, surface_height // 2 + (20 * scaler))
        #
        # surface.blit(level_font_surface, level_font_rect)

    graph = Graph()

    boxes = [Boxes() for box in range(4)]


    all_points = []
    point_data_view = []
    up_data, down_data, left_data, right_data = [], [], [], []
    for point in range(entries):

        if time_stamp_total[point] in time_stamp_success:
            point_data = (all_entries[point][-1], all_entries[point][2], all_entries[point][0], False)
            # point_data_view.append((all_entries[point][-1], all_entries[point][2], all_entries[point][0], True))
        else:
            point_data = (all_entries[point][-1], all_entries[point][2], all_entries[point][0], True)
            # point_data_view.append((all_entries[point][-1], all_entries[point][2], all_entries[point][0], False))

        # if all_entries[point][0] == "1":
        #     up_data.append((all_entries[point][-1], all_entries[point][2]))
        # elif all_entries[point][0] == "2":
        #     down_data.append((all_entries[point][-1], all_entries[point][2]))
        # elif all_entries[point][0] == "3":
        #     left_data.append((all_entries[point][-1], all_entries[point][2]))
        # else:
        #     right_data.append((all_entries[point][-1], all_entries[point][2]))

        all_points.append(Point(point_data))

    # print(f"point data:\n")
    # for entry in point_data_view:
    #     print(entry)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "s":
                    return

        mx, my = pygame.mouse.get_pos()


        clock.tick(fps)
        surface.fill(color.black)

        graph.draw_graph()

        for box in boxes:
            box.draw_box((mx, my))

        draw_margin()
        render_text()

        for point in all_points:
            point.draw_point()



        draw_line(entries_directions)

        pygame.display.update()

