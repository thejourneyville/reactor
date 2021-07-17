import pygame
import random


def run_reactor(surface, surface_width, surface_height, scaler, clock, fps):

    pygame.display.set_caption("REACTOR")

    # colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    lightgrey = (150, 150, 150)
    darkgrey = (100, 100, 100)
    red = (240, 17, 59)
    yellow = (255, 169, 0)
    orange = (255, 118, 0)
    purple = (82, 0, 106)


    wall_thinness = 10
    margin = 25
    margin_color = purple
    rehabilitate = 0



    class Doors:
        def __init__(self):
            self.width_TB = (surface_width // 2) - 1
            self.height_TB = surface_height // wall_thinness
            self.width_LR = surface_height // wall_thinness
            self.height_LR = (surface_height // 2) - 1
            self.speed = int(23 * scaler)
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

            rendered_margin = pygame.draw.rect(surface, margin_color, (0, 0, surface_width, surface_height), margin)

            return rendered_doors.append(rendered_margin)

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
            if self.rest:
                self.rest -= 1
            else:
                key = pygame.key.get_pressed()

                if key[pygame.K_UP] and not self.rest and self.switch == 0:
                    self.switch = 1
                if self.switch == 1:
                    self.ball.y -= self.speed
                    if self.ball.bottom < 0:
                        self.score += 1
                        self.ball.x, self.ball.y = self.x, self.y
                        self.switch = 0
                        self.rest = 10

                if key[pygame.K_DOWN] and not self.rest and self.switch == 0:
                    self.switch = 2
                if self.switch == 2:
                    self.ball.y += self.speed
                    if self.ball.top > surface_height:
                        self.score += 1
                        self.ball.x, self.ball.y = self.x, self.y
                        self.switch = 0
                        self.rest = 10

                if key[pygame.K_LEFT] and not self.rest and self.switch == 0:
                    self.switch = 3
                if self.switch == 3:
                    self.ball.x -= self.speed
                    if self.ball.right < 0:
                        self.score += 1
                        self.ball.x, self.ball.y = self.x, self.y
                        self.switch = 0
                        self.rest = 10

                if key[pygame.K_RIGHT] and not self.rest and self.switch == 0:
                    self.switch = 4
                if self.switch == 4:
                    self.ball.x += self.speed
                    if self.ball.left > surface_width:
                        self.score += 1
                        self.ball.x, self.ball.y = self.x, self.y
                        self.switch = 0
                        self.rest = 10

        def ball_coord_getter(self):
            return self.ball.center, self.switch

        def collision(self, bx, by, dx, dy):
            distance = (((dx - bx) ** 2) + ((dy - by) ** 2)) ** .5
            if distance <= self.radius:
                return True
            else:
                return False

        def ball_pulse(self, switch_state, current_color):
            if not lives:
                return False, 0

            if current_color >= 245:
                switch_state = False
            elif current_color <= 100:
                switch_state = True

            self.pulse_speed = int(50 // lives)
            if current_color + self.pulse_speed > 255:
                current_color = 255 - self.pulse_speed

            if not switch_state:
                return switch_state, current_color - self.pulse_speed
            elif switch_state:
                return switch_state, current_color + self.pulse_speed

        def draw_ball(self, color):
            pygame.draw.circle(
                surface,
                (59, 17, color),
                (self.ball.x + self.radius, self.ball.y + self.radius),
                self.radius,
                int(25 * scaler))


    # text rendered using blit
    def stats(total_points, lives_left, timer):

        font_style = "darkforest.ttf"
        font = pygame.font.Font(f"./{font_style}", int(20 * scaler))
        lives_font = pygame.font.Font(f"./{font_style}", int(75 * scaler))

        text_color = black
        timer_color = black
        if 10 < timer <= time_limit // 2:
            timer_color = orange
        elif timer <= 10:
            timer_color = red

        shot_accuracy = total_points[0]
        total_openings = total_points[-1]

        text_surface = font.render(f"shots made/total: {shot_accuracy}", True, text_color)
        text_surface1 = lives_font.render(str(lives_left), True, text_color)
        text_surface2 = font.render(str(timer), True, timer_color)
        text_surface3 = font.render(f"tries/openings: {total_openings}", True, text_color)

        text_rect = text_surface.get_rect()
        text_rect1 = text_surface1.get_rect()
        text_rect2 = text_surface2.get_rect()
        text_rect3 = text_surface3.get_rect()

        text_rect.centerx, text_rect.centery = surface_width // 2, surface_height // 2 + (130 * scaler)
        text_rect1.centerx, text_rect1.centery = surface_width // 2, surface_height // 2 + (5 * scaler)
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

        return f"{pass_throughs}/{total_tries} {percentage_1}", f"{total_tries}/{door_slides} {percentage_2}"


    doors = Doors()
    ball = Ball()

    rise = True
    ball_color = 0

    lives = 10
    score = 0
    collisions = 0

    time_limit = 60
    time_remaining = 0
    game_over = False

    start_ticks = pygame.time.get_ticks()  # starter tick

    while not game_over:

        clock.tick(fps)
        surface.fill(lightgrey)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "q":
                    game_over = True

        ball.launch()
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

        result_front = ball.collision(
            ball_coord[0],
            ball_coord[-1],
            all_doors_coords[switch - 1][x],
            all_doors_coords[switch - 1][y])

        result_back = ball.collision(
            ball_coord[0],
            ball_coord[-1],
            all_doors_coords[switch - 1][0],
            all_doors_coords[switch - 1][1])

        if result_front or result_back:
            lives -= 1
            collisions += 1
            margin_color = red

            if lives == 0:
                game_over = True

            else:
                ball = Ball()
                ball.rest = 10
                ball.score = score
        else:
            score = ball.score

        doors.draw_doors()

        if margin_color == red:
            rehabilitate += 1
            if rehabilitate == 5:
                margin_color = purple
                rehabilitate = 0

        rise, ball_color = ball.ball_pulse(rise, ball_color)
        ball.draw_ball(ball_color)

        accuracy_result = accuracy(score, collisions, doors.get_openings())
        if game_over:
            return accuracy_result, time_remaining

        stats(accuracy_result, lives, time_remaining)

        pygame.display.update()

        elapsed_seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)  # calculate how many seconds
        time_remaining = time_limit - elapsed_seconds
        if time_remaining < 0:  # if equal/less than 0 seconds close the game
            # game_over = True
            return accuracy_result, time_remaining


    print("game over!")
    print("final score: {}".format(score))
