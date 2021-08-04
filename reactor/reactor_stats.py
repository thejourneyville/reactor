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
    all_entries = success + fail
    success_directions = [entry[0] for entry in success]
    fail_directions = [entry[1] for entry in fail]
    success_times = [entry[2] for entry in success]
    fail_times = [entry[2] for entry in fail]
    all_times = success_times + fail_times
    print(f"all times: {all_times}")
    slowest_time = max(all_times)
    print(f"slowest time: {slowest_time}")
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
    time_stamp_total = time_stamp_success + time_stamp_fail


    # print(f"stats screen: {level}")
    # print("stats screen: current_react_data:")
    # print(f"door speed: {data['door_speed']}")
    print(f"total entries, successes, fails: {entries, successes, fails}")
    print(f"success directions: {success_directions}")
    print(f"fail_directions: {fail_directions}")
    print(f"success_times: {success_times}")
    print(f"fail times: {fail_times}")
    print(f"time stamp total: {time_stamp_total}")

    class Graph:
        def __init__(self):
            self.width = int(surface_width) - (margin // 2)
            self.height = int(surface_height) - (margin // 2)
            self.x_adjust = int(margin)
            self.y_adjust = int(margin)
            self.row_amount = (abs(fastest_success - slowest_fail) * .05)
            self.rows = self.height / self.row_amount
            self.cols_amount = time_elapsed
            self.cols = self.width / self.cols_amount
            self.gridline_width = 1
            self.gridline_color = color.darkgrey
            # self.true_point_radius = 10
            # self.point_radius = self.true_point_radius * scaler
            # self.point_up = pygame.Rect((self.x, self.y), (self.point_radius * 2, self.point_radius * 2))
            print(self.height)

        def draw_graph(self):
            for row in range(int(self.row_amount)):
                #rows
                pygame.draw.line(surface,
                                 self.gridline_color,
                                 (0, margin // 2 + self.rows * row),
                                 (surface_width, margin // 2 + self.rows * row),
                                 self.gridline_width)

            for col in range(int(self.cols_amount)):
                # cols
                pygame.draw.line(surface,
                                 self.gridline_color,
                                 (margin // 2 + self.cols * col, 0),
                                 (margin // 2 + self.cols * col, surface_height),
                                 self.gridline_width)

    class Point:
        def __init__(self, p):
            self.x = p[0] * graph.cols
            self.y = ((surface_height - margin * 2) / slowest_time) * p[1]
            self.color = [color.white, color.yellow, color.sky_blue, color.alert_red][p[2] - 1]
            self.result = p[-1]
            self.radius = 5
            self.ball = pygame.Rect((int(self.x), int(self.y)), (self.radius, self.radius))

        def draw_point(self):

            if self.result:
                pygame.draw.circle(
                    surface,
                    self.color,
                    (self.x + self.radius, self.y + self.radius),
                    self.radius)
            else:
                pygame.draw.circle(
                    surface,
                    self.color,
                    (self.x + self.radius, self.y + self.radius),
                    self.radius,
                    2)

    def draw_margin():
        pygame.draw.rect(surface, color.charcoal, (0, 0, surface_width, surface_height), margin)

    graph = Graph()

    all_points = []
    for point in range(entries):
        if time_stamp_total[point] in time_stamp_success:
            point_data = (all_entries[point][-1], all_entries[point][2], all_entries[point][0], True)
        else:
            point_data = (all_entries[point][-1], all_entries[point][2], all_entries[point][0], False)
        print(point_data)
        all_points.append(Point(point_data))

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
        for direction in coord_pos:
            surfaces.append((key_font.render(f"{direction[-1]}", True, color.white), coord_pos[direction[-1]]))

        rects = []
        # cont here

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

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "s":
                    return

        clock.tick(fps)
        surface.fill(color.black)

        graph.draw_graph()
        draw_margin()
        render_text()

        for point in all_points:
            point.draw_point()

        pygame.display.update()

