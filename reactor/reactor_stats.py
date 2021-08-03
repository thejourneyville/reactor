import pygame
import reactor_colors as color


def stats(surface, surface_width, surface_height, margin_color,
          scaler, clock, fps, level, current_react_data, time_elapsed):

    pygame.display.set_caption(f"PLAYER STATISTICS")
    margin = 30

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
    time_stamp_total = len(time_stamp_success) + len(time_stamp_fail)


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
            self.gridline_color = color.grid_lines
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
            self.y = ((surface_height - margin) / slowest_time) * p[1]
            self.color = [0, color.white, color.forest_green, color.sky_blue, color.alert_red][p[-1]]
            self.radius = 5
            self.ball = pygame.Rect((int(self.x), int(self.y)), (self.radius, self.radius))

        def draw_point(self):
            pygame.draw.circle(
                surface,
                self.color,
                (self.x + self.radius, self.y + self.radius),
                self.radius)

    def draw_margin():
        pygame.draw.rect(surface, margin_color, (0, 0, surface_width, surface_height), margin)

    graph = Graph()

    all_points = []
    for point in range(entries):

        point_data = (all_entries[point][-1], all_entries[point][2], all_entries[point][0])
        print(point_data)
        all_points.append(Point(point_data))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "s":
                    return

        clock.tick(fps)
        surface.fill(color.lightgrey)

        graph.draw_graph()
        draw_margin()

        for point in all_points:
            point.draw_point()

        pygame.display.update()

