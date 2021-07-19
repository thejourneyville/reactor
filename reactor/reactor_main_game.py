import pygame
import random


def run_reactor(surface, surface_width, surface_height, margin, scaler, clock, fps):

    pygame.display.set_caption("REACTOR")

    # colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    lightgrey = (150, 150, 150)
    darkgrey = (100, 100, 100)
    red = (240, 17, 59)
    blue = (59, 17, 240)
    yellow = (255, 169, 0)
    orange = (255, 118, 0)
    purple = (82, 0, 106)

    wall_thinness = 10

    margin_color = purple
    margin_switch = "purple"
    rehabilitate = 0
    rehab_duration = 100


    class Doors:
        def __init__(self):
            self.width_TB = (surface_width // 2) - 1
            self.height_TB = surface_height // wall_thinness
            self.width_LR = surface_height // wall_thinness
            self.height_LR = (surface_height // 2) - 1
            self.speed = int(26 * scaler)
            self.switcher = None
            self.openings = 0
            self.rest_period = 0
            self.current_rest_period = -100
            self.random_range = random.randint(50, 200)

            # top doors
            self.x_T_L = 0
            self.y_T_L = 0
            self.x_T_R = (surface_width // 2) + 2
            self.y_T_R = 0
            self.rect_T_L = pygame.Rect(self.x_T_L, self.y_T_L, self.width_TB, self.height_TB)
            self.rect_T_R = pygame.Rect(self.x_T_R, self.y_T_R, self.width_TB, self.height_TB)
            self.direction_T = 0
            self.rest_period_T = 0
            self.rest_T = True

            # bottom doors
            self.x_B_L = 0
            self.y_B_L = surface_height - (surface_height // wall_thinness)
            self.x_B_R = (surface_width // 2) + 2
            self.y_B_R = surface_height - (surface_height // wall_thinness)
            self.rect_B_L = pygame.Rect(self.x_B_L, self.y_B_L, self.width_TB, self.height_TB)
            self.rect_B_R = pygame.Rect(self.x_B_R, self.y_B_R, self.width_TB, self.height_TB)
            self.direction_B = 0
            self.rest_period_B = 0
            self.rest_B = True

            # left doors
            self.x_L_T = 0
            self.y_L_T = 0
            self.x_L_B = 0
            self.y_L_B = (surface_height // 2) + 2
            self.rect_L_T = pygame.Rect(self.x_L_T, self.y_L_T, self.width_LR, self.height_LR)
            self.rect_L_B = pygame.Rect(self.x_L_B, self.y_L_B, self.width_LR, self.height_LR)
            self.direction_L = 0
            self.rest_period_L = 0
            self.rest_L = True

            # right doors
            self.x_R_T = surface_width - self.width_LR
            self.y_R_T = 0
            self.x_R_B = surface_width - self.width_LR
            self.y_R_B = (surface_height // 2) + 2
            self.rect_R_T = pygame.Rect(self.x_R_T, self.y_R_T, self.width_LR, self.height_LR)
            self.rect_R_B = pygame.Rect(self.x_R_B, self.y_R_B, self.width_LR, self.height_LR)
            self.direction_R = 0
            self.rest_period_R = 0
            self.rest_R = True

        def slide_T(self):

            if self.switcher is None:
                if self.rest_T:
                    self.current_rest_period += 1

                    if self.current_rest_period > self.rest_period:
                        self.current_rest_period = 0
                        self.rest_T = False

                if not self.rest_T:
                    result_t = random.randint(1, self.random_range)
                    if result_t == 1:
                        self.rest_R, self.rest_L, self.rest_B = True, True, True
                        self.switcher = "top"
                        self.direction_T = 1

            elif self.switcher == "top":

                if self.rect_T_L.right > 0 and self.direction_T == 1:
                    self.rect_T_L.x -= self.speed
                    self.rect_T_R.x += self.speed

                elif self.rect_T_L.right <= 0:
                    self.direction_T = -1

                if self.direction_T == -1:
                    self.rect_T_L.x += self.speed
                    self.rect_T_R.x -= self.speed

                    if self.rect_T_L.left == 0:
                        self.direction_T = 0
                        self.rest_T = True
                        self.current_rest_period = -200
                        self.openings += 1
                        self.switcher = None

            return self.rect_T_L.right, self.rect_T_L.topright[-1] - margin, self.rect_T_L.bottomright[-1]

        def slide_B(self):

            if self.switcher is None:
                if self.rest_B:
                    self.current_rest_period += 1

                    if self.current_rest_period > self.rest_period:
                        self.current_rest_period = 0
                        self.rest_B = False

                if not self.rest_B:
                    result_b = random.randint(1, self.random_range)
                    if result_b == 1:
                        self.rest_R, self.rest_L, self.rest_T = True, True, True
                        self.switcher = "bottom"
                        self.direction_B = 1

            elif self.switcher == "bottom":

                if self.rect_B_L.right > 0 and self.direction_B == 1:
                    self.rect_B_L.x -= self.speed
                    self.rect_B_R.x += self.speed

                elif self.rect_B_L.right <= 0:
                    self.direction_B = -1

                if self.direction_B == -1:
                    self.rect_B_L.x += self.speed
                    self.rect_B_R.x -= self.speed

                    if self.rect_B_L.left == 0:
                        self.direction_B = 0
                        self.rest_B = True
                        self.current_rest_period = -200
                        self.openings += 1
                        self.switcher = None

            return self.rect_B_L.right, self.rect_B_L.bottomright[-1] - margin, self.rect_B_L.topright[-1]

        def slide_L(self):

            if self.switcher is None:
                if self.rest_L:
                    self.current_rest_period += 1

                    if self.current_rest_period > self.rest_period:
                        self.current_rest_period = 0
                        self.rest_L = False

                if not self.rest_L:
                    result_l = random.randint(1, self.random_range)
                    if result_l == 1:
                        self.rest_R, self.rest_B, self.rest_T = True, True, True
                        self.switcher = "left"
                        self.direction_L = 1

            elif self.switcher == "left":

                if self.rect_L_T.bottom > 0 and self.direction_L == 1:
                    self.rect_L_T.y -= self.speed
                    self.rect_L_B.y += self.speed

                elif self.rect_L_T.bottom <= 0:
                    self.direction_L = -1

                if self.direction_L == -1:
                    self.rect_L_T.y += self.speed
                    self.rect_L_B.y -= self.speed

                    if self.rect_L_T.top == 0:
                        self.direction_L = 0
                        self.rest_L = True
                        self.current_rest_period = -200
                        self.openings += 1
                        self.switcher = None

            return self.rect_L_T.bottomleft[0] + margin, self.rect_L_T.bottom, self.rect_L_T.bottomright[0]

        def slide_R(self):

            if self.switcher is None:
                if self.rest_R:
                    self.current_rest_period += 1

                    if self.current_rest_period > self.rest_period:
                        self.current_rest_period = 0
                        self.rest_R = False

                if not self.rest_R:
                    result_r = random.randint(1, self.random_range)
                    if result_r == 1:
                        self.rest_L, self.rest_B, self.rest_T = True, True, True
                        self.switcher = "right"
                        self.direction_R = 1

            elif self.switcher == "right":

                if self.rect_R_T.bottom > 0 and self.direction_R == 1:
                    self.rect_R_T.y -= self.speed
                    self.rect_R_B.y += self.speed

                elif self.rect_R_T.bottom <= 0:
                    self.direction_R = -1

                if self.direction_R == -1:
                    self.rect_R_T.y += self.speed
                    self.rect_R_B.y -= self.speed

                    if self.rect_R_T.top == 0:
                        self.direction_R = 0
                        self.rest_R = True
                        self.current_rest_period = -200
                        self.openings += 1
                        self.switcher = None

            return self.rect_R_T.bottomright[0] - margin, self.rect_R_T.bottom, self.rect_R_T.bottomleft[0]

        def draw_doors(self):
            all_doors = [self.rect_T_L, self.rect_T_R, self.rect_B_L, self.rect_B_R,
                         self.rect_L_T, self.rect_L_B, self.rect_R_T, self.rect_R_B]
            rendered_doors = [pygame.draw.rect(surface, black, door) for door in all_doors]

            return rendered_doors

        def get_openings(self):
            return self.openings

    class Ball:
        def __init__(self):
            self.radius = 100 * scaler
            self.x = (surface_width // 2) - self.radius
            self.y = (surface_height // 2) - self.radius
            self.ball = pygame.Rect((self.x, self.y), (self.radius * 2, self.radius * 2))
            self.speed = int(50 * scaler)
            self.switch = 0
            self.rest = 0
            self.score = 0
            self.pulse_speed = 10

        def launch(self):

            success_shot = False
            if self.rest:
                self.rest -= 1
            else:
                key = pygame.key.get_pressed()

                if key[pygame.K_UP] and not self.rest and self.switch == 0:
                    self.switch = 1
                if self.switch == 1:
                    self.ball.y -= self.speed
                    if self.ball.bottom < 0:
                        success_shot = True
                        self.score += 1
                        self.ball.x, self.ball.y = self.x, self.y
                        self.switch = 0
                        self.rest = 10

                if key[pygame.K_DOWN] and not self.rest and self.switch == 0:
                    self.switch = 2
                if self.switch == 2:
                    self.ball.y += self.speed
                    if self.ball.top > surface_height:
                        success_shot = True
                        self.score += 1
                        self.ball.x, self.ball.y = self.x, self.y
                        self.switch = 0
                        self.rest = 10

                if key[pygame.K_LEFT] and not self.rest and self.switch == 0:
                    self.switch = 3
                if self.switch == 3:
                    self.ball.x -= self.speed
                    if self.ball.right < 0:
                        success_shot = True
                        self.score += 1
                        self.ball.x, self.ball.y = self.x, self.y
                        self.switch = 0
                        self.rest = 10

                if key[pygame.K_RIGHT] and not self.rest and self.switch == 0:
                    self.switch = 4
                if self.switch == 4:
                    self.ball.x += self.speed
                    if self.ball.left > surface_width:
                        success_shot = True
                        self.score += 1
                        self.ball.x, self.ball.y = self.x, self.y
                        self.switch = 0
                        self.rest = 10

            return success_shot

        def ball_coord_getter(self):
            return self.ball.center, self.switch

        def collision(self, bx, by, dx, dy):
            distance = (((dx - bx) ** 2) + ((dy - by) ** 2)) ** .5

            if distance <= self.radius:
                return True, (dx, dy)
            else:
                return False, None

        def ball_pulse(self, switch_state, current_color):
            if not lives:
                return False, 0

            if current_color >= 245:
                switch_state = False
            elif current_color <= 100:
                switch_state = True

            if lives == 10:
                self.pulse_speed = 1
            else:
                self.pulse_speed = int(25 // lives)
            if current_color + self.pulse_speed > 255:
                current_color = 255 - self.pulse_speed

            if not switch_state:
                return switch_state, current_color - self.pulse_speed
            elif switch_state:
                return switch_state, current_color + self.pulse_speed

        def draw_ball(self, color):

            blue_shift = color
            red_shift = 255 + (color * -1) + self.pulse_speed

            if red_shift > 200:
                red_shift = 200
            if blue_shift > 255:
                blue_shift = 255

            pygame.draw.circle(
                surface,
                (red_shift, 0, blue_shift),
                (self.ball.x + self.radius, self.ball.y + self.radius),
                self.radius,
                int(25 * scaler))

            return red_shift, 0, blue_shift

        @staticmethod
        def get_ball_color(current):
            return current

    def draw_margin(color, rehab):
        # red = (240, 17, 59)
        # blue = (59, 17, 240)
        # purple = (82, 0, 106)

        red_purple_shift = abs(red[0] - purple[0]) / rehab_duration, \
                           abs(red[1] - purple[1]) / rehab_duration, \
                           abs(red[2] - purple[2]) / rehab_duration
        blue_purple_shift = abs(blue[0] - purple[0]) / rehab_duration, \
                            abs(blue[1] - purple[1]) / rehab_duration, \
                            abs(blue[2] - purple[2]) / rehab_duration

        if rehab < rehab_duration:
            if color == red:

                shift = red_purple_shift
                color = (color[0] - shift[0] * rehab,
                         color[1] - shift[1] * rehab,
                         color[2] + shift[2] * rehab)
            elif color == blue:

                shift = blue_purple_shift
                color = (color[0] + shift[0] * rehab,
                         color[1] - shift[1] * rehab,
                         color[2] - shift[2] * rehab)

        color = int(color[0]), int(color[1]), int(color[2])

        return pygame.draw.rect(surface, color, (0, 0, surface_width, surface_height), margin)

    # text rendered using blit
    def stats(total_points, lives_left, timer):

        font_style = "darkforest.ttf"
        lives_stlye = "SF Square Head Bold.ttf"
        font = pygame.font.Font(f"./{font_style}", int(20 * scaler))
        lives_font = pygame.font.Font(f"./{lives_stlye}", int(75 * scaler))

        text_color = black
        timer_color = black
        lives_color = black
        if timer <= 10:
            timer_color = red

        if lives_left <= 3:
            lives_color = red

        shot_accuracy = total_points[0]
        total_openings = total_points[-1]

        text_surface = font.render(f"shots made/total: {shot_accuracy}", True, text_color)
        text_surface1 = lives_font.render(str(lives_left), True, lives_color)
        text_surface2 = font.render(str(timer), True, timer_color)
        text_surface3 = font.render(f"tries/openings: {total_openings}", True, text_color)

        text_rect = text_surface.get_rect()
        text_rect1 = text_surface1.get_rect()
        text_rect2 = text_surface2.get_rect()
        text_rect3 = text_surface3.get_rect()

        text_rect.centerx, text_rect.centery = surface_width // 2, surface_height // 2 + (130 * scaler)
        text_rect1.centerx, text_rect1.centery = surface_width // 2, surface_height // 2
        text_rect2.centerx, text_rect2.centery = surface_width // 2, surface_height // 2 + (40 * scaler)
        text_rect3.centerx, text_rect3.centery = surface_width // 2, surface_height // 2 - (130 * scaler)

        surface.blit(text_surface, text_rect)
        surface.blit(text_surface1, text_rect1)
        surface.blit(text_surface2, text_rect2)
        surface.blit(text_surface3, text_rect3)

    def accuracy(pass_throughs, fails, door_slides):

        total_tries = pass_throughs + fails

        if not total_tries:
            percentage_1 = 0.0
        else:
            percentage_1 = round((pass_throughs / total_tries) * 100, 1)

        if not door_slides:
            percentage_2 = 0.0
        else:
            percentage_2 = round((total_tries / door_slides) * 100, 1)
        print(pass_throughs, fails, total_tries, door_slides)
        return f"{pass_throughs}/{total_tries} {percentage_1}", f"{total_tries}/{door_slides} {percentage_2}"

    def explosion(coords, particles):

        explode_x =  coords[0]
        explode_y = coords[-1]
        explode_speed_x = random.choice([-15, -3, -3, -2])
        explode_speed_y = (random.randrange(20) / 10 - 1) * 20
        shrapnel_size = random.randint(20, 23)
        shrapnel_exists = True

        for i in range(50):
            particles.append([
            [coords[0], coords[-1]],
            [random.choice(list(range(-20, 20))), random.choice(list(range(-20, 20)))],
            random.randint(15, 20),
            True
        ])

        return particles

    def anim_explosion(particles, shrapnal_color):

        for current in particles:
            current[0][0] += current[1][0] * 2
            current[0][1] += current[1][1] * 2
            current[2] -= random.choice([.1, .3, .5, .7, 1])
            current[1][1] += 1

            pygame.draw.rect(surface, shrapnal_color, (int(current[0][0]), int(current[0][1]), int(current[2]), int(current[2])))

            if current[2] <= 0:
                current[-1] = False

        for current in all_particles:
            if not current[-1]:
                all_particles.remove(current)

        return particles


    doors = Doors()
    ball = Ball()

    rise = True
    ball_color = 200

    lives = 10
    score = 0
    collisions = 0
    particle, all_particles, modded_particles = [], [], []
    go_explosion = False
    current_ball_color = blue
    ball_color_explosion = (0, 0, 0)

    time_limit = 999
    time_remaining = 0
    game_over = False

    start_ticks = pygame.time.get_ticks()  # starter tick

    while True:

        clock.tick(fps)
        surface.fill(lightgrey)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "q":
                    game_over = True

        success = ball.launch()
        ball_coord, switch = ball.ball_coord_getter()

        door_T_x, door_T_y, door_T_y_front_side = doors.slide_T()
        door_B_x, door_B_y, door_B_y_front_side = doors.slide_B()
        door_L_x, door_L_y, door_L_x_front_side = doors.slide_L()
        door_R_x, door_R_y, door_R_x_front_side = doors.slide_R()

        all_doors_coords = [(door_T_x, door_T_y, door_T_y_front_side),
                            (door_B_x, door_B_y, door_B_y_front_side),
                            (door_L_x, door_L_y, door_L_x_front_side),
                            (door_R_x, door_R_y, door_R_x_front_side)]

        if (switch - 1) < 2: x, y = 0, -1
        else: x, y = -1, 1

        result_front, result_back = False, False
        result_front, collide_location = ball.collision(
            ball_coord[0],
            ball_coord[-1],
            all_doors_coords[switch - 1][x],
            all_doors_coords[switch - 1][y])

        if not result_front:
            result_back, collide_location = ball.collision(
                ball_coord[0],
                ball_coord[-1],
                all_doors_coords[switch - 1][0],
                all_doors_coords[switch - 1][1])

        if not game_over and any([result_front, result_back]):
            lives -= 1
            collisions += 1
            margin_color = red
            rehabilitate = 1

            all_particles = explosion(collide_location, all_particles)
            ball_color_explosion = ball.get_ball_color(current_ball_color)

            if lives == 0:
                game_over = True

            else:
                ball = Ball()
                ball.rest = 10
                ball.score = score

        if success:
            margin_color = blue
            rehabilitate = 1
            score = ball.score
            success = False

        if margin_color == red:
            if margin_switch == "blue":
                margin_switch = "red"
            else:
                margin_switch = "red"
                rehabilitate += 1
            if rehabilitate == rehab_duration:
                margin_color = purple
                margin_switch = "purple"
                rehabilitate = 1
        elif margin_color == blue:
            if margin_switch == "red":
                margin_switch = "blue"
            else:
                margin_switch = "blue"
                rehabilitate += 1
            if rehabilitate == rehab_duration:
                margin_color = purple
                margin_switch = "purple"
                rehabilitate = 1

        if not game_over:
            accuracy_result = accuracy(score, collisions, doors.get_openings())
            doors.draw_doors()
            rise, ball_color = ball.ball_pulse(rise, ball_color)
            current_ball_color = ball.draw_ball(ball_color)
            stats(accuracy_result, lives, time_remaining)

        if game_over:
            if len(all_particles) <= 1:
                return accuracy_result, time_remaining
        elif time_remaining < 0:  # if equal/less than 0 seconds close the game
            if len(all_particles) <= 1:
                return accuracy_result, time_remaining

        all_particles = anim_explosion(all_particles, ball_color_explosion)

        draw_margin(margin_color, rehabilitate)

        pygame.display.update()

        elapsed_seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)  # calculate how many seconds
        time_remaining = time_limit - elapsed_seconds



    print("game over!")
    print("final score: {}".format(score))
