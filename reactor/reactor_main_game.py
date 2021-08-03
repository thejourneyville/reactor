import pygame
import random
from collections import deque
import reactor_colors as color


def run_reactor(surface, surface_width, surface_height, margin, margin_color,
                scaler, clock, fps,
                door_speed, score_goal, time_limit):

    # variables
    pygame.display.set_caption("REACTOR")
    door_thinness = 10
    margin_return_nominal_state = 0
    margin_return_nominal_state_duration = 25
    disc_color_rising = True
    disc_color = 200
    lives = 2
    score = 0
    collisions = 0
    collision_result_front, collision_result_back = False, False
    particle, all_particles, modded_particles = [], [], []
    current_disc_color = color.blue
    disc_explosion_color = (0, 0, 0)
    timer_marker = pygame.time.get_ticks()  # starter tick
    current_react_data = {}
    react_fade_speed = .25
    react_movement_speed = .25
    shadow_delay = 1
    shadow_coord_1 = deque([], maxlen=shadow_delay)
    shadow_coord_2 = deque([], maxlen=shadow_delay * 2)
    shadow_coord_3 = deque([], maxlen=shadow_delay * 3)
    shadow_coord_4 = deque([], maxlen=shadow_delay * 4)
    shadow_coord_5 = deque([], maxlen=shadow_delay * 5)
    shadow_coord_6 = deque([], maxlen=shadow_delay * 6)
    shadow_coord_7 = deque([], maxlen=shadow_delay * 7)
    shadow_coord_8 = deque([], maxlen=shadow_delay * 8)
    shadow_coord_9 = deque([], maxlen=shadow_delay * 9)
    shadow_coord_10 = deque([], maxlen=shadow_delay * 10)
    all_shadows = [shadow_coord_10,
                   shadow_coord_9,
                   shadow_coord_8,
                   shadow_coord_7,
                   shadow_coord_6,
                   shadow_coord_5,
                   shadow_coord_4,
                   shadow_coord_3,
                   shadow_coord_2,
                   shadow_coord_1]
    game_over = False

    class Doors:
        def __init__(self):
            self.width_TB = (surface_width // 2) - 1
            self.height_TB = surface_height // door_thinness
            self.width_LR = surface_height // door_thinness
            self.height_LR = (surface_height // 2) - 1
            self.true_door_speed = door_speed
            self.door_speed = int(self.true_door_speed * scaler)
            self.switcher = 0
            self.openings = 0
            self.rest_period = 25
            self.current_rest_period = -100
            self.random_range = random.randint(10, 100)
            self.locked = False
            self.start_mark_open = 0
            self.start_timer = True
            self.last_open = 0

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
            self.y_B_L = surface_height - (surface_height // door_thinness)
            self.x_B_R = (surface_width // 2) + 2
            self.y_B_R = surface_height - (surface_height // door_thinness)
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

            if self.switcher == 0:
                if self.rest_T:
                    self.current_rest_period += 1

                    if self.current_rest_period > self.rest_period:
                        self.current_rest_period = 0
                        self.rest_T = False

                if not self.rest_T:
                    result_t = random.randint(1, random.randint(10, 500))
                    if result_t == 1:
                        self.rest_R, self.rest_L, self.rest_B = True, True, True
                        self.switcher = 1
                        self.direction_T = 1

            elif self.switcher == 1:

                if self.rect_T_L.right > 0 and self.direction_T == 1 and not self.locked:

                    if self.start_timer:
                        self.start_mark_open = pygame.time.get_ticks()
                        self.start_timer = False
                    self.last_open = self.switcher

                    self.rect_T_L.x -= self.door_speed
                    self.rect_T_R.x += self.door_speed

                elif self.rect_T_L.right <= 0:
                    self.direction_T = -1

                if self.direction_T == -1:
                    self.rect_T_L.x += self.door_speed
                    self.rect_T_R.x -= self.door_speed

                    if self.rect_T_L.left == 0:
                        self.direction_T = 0
                        self.rest_T = True
                        self.current_rest_period = 0
                        self.openings += 1
                        self.switcher = 0
                        self.start_timer = True

            return self.rect_T_L.right, self.rect_T_L.topright[-1] - margin, self.rect_T_L.bottomright[-1]

        def slide_B(self):

            if self.switcher == 0:
                if self.rest_B:
                    self.current_rest_period += 1

                    if self.current_rest_period > self.rest_period:
                        self.current_rest_period = 0
                        self.rest_B = False

                if not self.rest_B:
                    result_b = random.randint(1, random.randint(10, 500))
                    if result_b == 1:
                        self.rest_R, self.rest_L, self.rest_T = True, True, True
                        self.switcher = 2
                        self.direction_B = 1

            elif self.switcher == 2:

                if self.rect_B_L.right > 0 and self.direction_B == 1 and not self.locked:

                    if self.start_timer:
                        self.start_mark_open = pygame.time.get_ticks()
                        self.start_timer = False
                    self.last_open = self.switcher

                    self.rect_B_L.x -= self.door_speed
                    self.rect_B_R.x += self.door_speed

                elif self.rect_B_L.right <= 0:
                    self.direction_B = -1

                if self.direction_B == -1:
                    self.rect_B_L.x += self.door_speed
                    self.rect_B_R.x -= self.door_speed

                    if self.rect_B_L.left == 0:
                        self.direction_B = 0
                        self.rest_B = True
                        self.current_rest_period = 0
                        self.openings += 1
                        self.switcher = 0
                        self.start_timer = True

            return self.rect_B_L.right, self.rect_B_L.bottomright[-1] - margin, self.rect_B_L.topright[-1]

        def slide_L(self):

            if self.switcher == 0:
                if self.rest_L:
                    self.current_rest_period += 1

                    if self.current_rest_period > self.rest_period:
                        self.current_rest_period = 0
                        self.rest_L = False

                if not self.rest_L:
                    result_l = random.randint(1, random.randint(10, 500))
                    if result_l == 1:
                        self.rest_R, self.rest_B, self.rest_T = True, True, True
                        self.switcher = 3
                        self.direction_L = 1

            elif self.switcher == 3:

                if self.rect_L_T.bottom > 0 and self.direction_L == 1 and not self.locked:

                    if self.start_timer:
                        self.start_mark_open = pygame.time.get_ticks()
                        self.start_timer = False
                    self.last_open = self.switcher

                    self.rect_L_T.y -= self.door_speed
                    self.rect_L_B.y += self.door_speed

                elif self.rect_L_T.bottom <= 0:
                    self.direction_L = -1

                if self.direction_L == -1:
                    self.rect_L_T.y += self.door_speed
                    self.rect_L_B.y -= self.door_speed

                    if self.rect_L_T.top == 0:
                        self.direction_L = 0
                        self.rest_L = True
                        self.current_rest_period = 0
                        self.openings += 1
                        self.switcher = 0
                        self.start_timer = True

            return self.rect_L_T.bottomleft[0] + margin, self.rect_L_T.bottom, self.rect_L_T.bottomright[0]

        def slide_R(self):

            if self.switcher == 0:
                if self.rest_R:
                    self.current_rest_period += 1

                    if self.current_rest_period > self.rest_period:
                        self.current_rest_period = 0
                        self.rest_R = False

                if not self.rest_R:
                    result_r = random.randint(1, random.randint(10, 500))
                    if result_r == 1:
                        self.rest_L, self.rest_B, self.rest_T = True, True, True
                        self.switcher = 4
                        self.direction_R = 1

            elif self.switcher == 4:

                if self.rect_R_T.bottom > 0 and self.direction_R == 1 and not self.locked:

                    if self.start_timer:
                        self.start_mark_open = pygame.time.get_ticks()
                        self.start_timer = False
                    self.last_open = self.switcher

                    self.rect_R_T.y -= self.door_speed
                    self.rect_R_B.y += self.door_speed

                elif self.rect_R_T.bottom <= 0:
                    self.direction_R = -1

                if self.direction_R == -1:
                    self.rect_R_T.y += self.door_speed
                    self.rect_R_B.y -= self.door_speed

                    if self.rect_R_T.top == 0:
                        self.direction_R = 0
                        self.rest_R = True
                        self.current_rest_period = 0
                        self.openings += 1
                        self.switcher = 0
                        self.start_timer = True

            return self.rect_R_T.bottomright[0] - margin, self.rect_R_T.bottom, self.rect_R_T.bottomleft[0]

        def draw_doors(self):
            all_doors = [self.rect_T_L, self.rect_T_R, self.rect_B_L, self.rect_B_R,
                         self.rect_L_T, self.rect_L_B, self.rect_R_T, self.rect_R_B]
            return [pygame.draw.rect(surface, color.doors_color, door) for door in all_doors]

        def get_openings(self):
            return self.openings

    class Ball:
        def __init__(self):
            self.true_disc_radius_size = 100
            self.disc_radius_size = self.true_disc_radius_size * scaler
            self.x = (surface_width // 2) - self.disc_radius_size
            self.y = (surface_height // 2) - self.disc_radius_size
            self.ball = pygame.Rect((self.x, self.y), (self.disc_radius_size * 2, self.disc_radius_size * 2))
            self.true_disc_speed = 50
            self.disc_speed = int(self.true_disc_speed * scaler)
            self.switch = 0
            self.rest = 100
            self.score = 0
            self.pulse_speed = 10
            self.start_mark_close = 0
            self.start_timer = True

        def launch(self):

            success_shot = False
            last_direction = 0

            if self.rest:
                self.rest -= 1

            else:

                pressed_key = pygame.key.get_pressed()  # creates tuple of all keys (0) and detects key pressed (1)

                if self.switch == 0:
                    if pressed_key[pygame.K_UP]:

                        if doors.start_mark_open:
                            if self.start_timer:
                                self.start_mark_close = pygame.time.get_ticks() - doors.start_mark_open
                                self.start_timer = False
                        self.switch = 1

                    elif pressed_key[pygame.K_DOWN]:

                        if doors.start_mark_open:
                            if self.start_timer:
                                self.start_mark_close = pygame.time.get_ticks() - doors.start_mark_open
                                self.start_timer = False
                        self.switch = 2

                    elif pressed_key[pygame.K_LEFT]:

                        if doors.start_mark_open:
                            if self.start_timer:
                                self.start_mark_close = pygame.time.get_ticks() - doors.start_mark_open
                                self.start_timer = False
                        self.switch = 3

                    elif pressed_key[pygame.K_RIGHT]:

                        if doors.start_mark_open:
                            if self.start_timer:
                                self.start_mark_close = pygame.time.get_ticks() - doors.start_mark_open
                                self.start_timer = False
                        self.switch = 4

                if self.switch == 1:
                    self.ball.y -= self.disc_speed
                elif self.switch == 2:
                    self.ball.y += self.disc_speed
                elif self.switch == 3:
                    self.ball.x -= self.disc_speed
                elif self.switch == 4:
                    self.ball.x += self.disc_speed

                if any([self.ball.top > surface_height,
                        self.ball.bottom < 0,
                        self.ball.left > surface_width,
                        self.ball.right < 0]):
                    success_shot = True
                    self.score += 1
                    self.ball.x, self.ball.y = self.x, self.y
                    last_direction = self.switch
                    self.switch = 0
                    self.rest = 10
                    self.start_timer = True

            return success_shot, max(self.switch, last_direction), self.ball.center

        def collision(self, bx, by, dx, dy):
            distance = (((dx - bx) ** 2) + ((dy - by) ** 2)) ** .5

            if distance <= self.disc_radius_size:
                return True, (dx, dy)
            else:
                return False, (dx, dy)

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

        def draw_ball(self, current_color):

            blue_shift = current_color
            red_shift = 255 + (current_color * -1) + self.pulse_speed

            if red_shift > 200:
                red_shift = 200
            if blue_shift > 255:
                blue_shift = 255

            pygame.draw.circle(
                surface,
                (red_shift, 0, blue_shift),
                (self.ball.x + self.disc_radius_size, self.ball.y + self.disc_radius_size),
                self.disc_radius_size,
                int(35 * scaler))

            return red_shift, 0, blue_shift

        @staticmethod
        def get_ball_color(current):
            return current

        def shadow(self, shadow_color):

            diff_r = shadow_color[0] - color.background[0]
            diff_g = shadow_color[1] - color.background[1]
            diff_b = shadow_color[2] - color.background[2]
            divisor = len(all_shadows)
            incrementor = [abs(diff_r / divisor), abs(diff_g / divisor), abs(diff_b / divisor)]

            r, g, b = shadow_color[0], shadow_color[1], shadow_color[2]
            all_colors = []
            for _ in range(len(all_shadows)):
                if diff_r < 0:
                    r += (incrementor[0])
                else:
                    r -= (incrementor[0])

                if diff_g < 0:
                    g += (incrementor[1])
                else:
                    g -= (incrementor[1])

                if diff_b < 0:
                    b += (incrementor[2])
                else:
                    b -= (incrementor[2])

                output_color = (int(r), int(g), int(b))
                all_colors.append(output_color)

            for idx, shadow in enumerate(all_shadows):
                shadow.append((self.ball.x, self.ball.y))
                pygame.draw.circle(
                    surface,
                    all_colors[(len(all_shadows) - 1) - idx],
                    (shadow[0][0] + self.disc_radius_size, shadow[0][-1] + self.disc_radius_size),
                    self.disc_radius_size,
                    int((idx + 1) ** 1.3))

    def draw_margin(m_color, rehab):
        # red = (240, 17, 59)
        # blue = (59, 17, 240)
        # purple = (82, 0, 106)
        r, g, b = m_color[0], m_color[1], m_color[2]
        if rehab < margin_return_nominal_state_duration:

            fail_nominal_shift = \
                (abs(color.fail_color[0] - color.margin_color[0]) / margin_return_nominal_state_duration,
                 abs(color.fail_color[1] - color.margin_color[1]) / margin_return_nominal_state_duration,
                 abs(color.fail_color[2] - color.margin_color[2]) / margin_return_nominal_state_duration)
            success_nominal_shift = \
                (abs(color.success_color[0] - color.margin_color[0]) / margin_return_nominal_state_duration,
                 abs(color.success_color[1] - color.margin_color[1]) / margin_return_nominal_state_duration,
                 abs(color.success_color[2] - color.margin_color[2]) / margin_return_nominal_state_duration)

            shift = (0, 0, 0)
            if m_color == color.fail_color:
                shift = fail_nominal_shift
            elif m_color == color.success_color:
                shift = success_nominal_shift

            if m_color[0] > color.margin_color[0]:
                r = m_color[0] - shift[0] * rehab
            else:
                r = m_color[0] + shift[0] * rehab

            if m_color[1] > color.margin_color[1]:
                g = m_color[1] - shift[1] * rehab
            else:
                g = m_color[1] + shift[1] * rehab

            if m_color[2] > color.margin_color[2]:
                b = m_color[2] - shift[2] * rehab
            else:
                b = m_color[2] + shift[2] * rehab

        m_color = int(r), int(g), int(b)

        return pygame.draw.rect(surface, m_color, (0, 0, surface_width, surface_height), margin)

    # text rendered using blit
    def stats(total_points, lives_left, time_left):
        font_style = "darkforest.ttf"
        lives_style = "SF Square Head Bold.ttf"
        font = pygame.font.Font(f"./{font_style}", int(20 * scaler))
        lives_font = pygame.font.Font(f"./{lives_style}", int(75 * scaler))

        text_color = color.doors_color
        timer_color = color.doors_color
        lives_color = color.doors_color
        if time_left <= 10:
            timer_color = color.fail_color

        if lives_left <= 3:
            lives_color = color.fail_color

        shot_accuracy = total_points[0]
        total_openings = total_points[-1]

        text_surface = font.render(f"shots made/total: {shot_accuracy}", True, text_color)
        text_surface1 = lives_font.render(str(lives_left), True, lives_color)
        text_surface2 = font.render(str(time_left), True, timer_color)
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

        if time_remaining >= 0:
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
        # print(pass_throughs, fails, total_tries, door_slides)
        return f"{pass_throughs}/{total_tries} {percentage_1}", f"{total_tries}/{door_slides} {percentage_2}"

    def build_reaction_data(total, success_fail, reaction_time, disc_direction, door):

        total.setdefault("door_speed", doors.true_door_speed)
        total.setdefault("disc_speed", ball.true_disc_speed)
        total.setdefault("disc_size", ball.true_disc_radius_size)
        total.setdefault("success", [])
        total.setdefault("fail", [])
        total.setdefault("last_shot_made", success_fail)

        y_axis_movement = 0
        starting_color_success = color.success_color
        starting_color_fail = color.fail_color
        current_timer = round(time_remaining_decimal, 2)  # pulled from timer function

        if success_fail:
            total["success"].append([disc_direction,
                                     door,
                                     reaction_time,
                                     y_axis_movement,
                                     starting_color_success,
                                     round(time_limit - current_timer, 2)])
            total["last_shot_made"] = True
        else:
            total["fail"].append([disc_direction,
                                  door, reaction_time,
                                  y_axis_movement,
                                  starting_color_fail,
                                  round(time_limit - current_timer, 2)])
            total["last_shot_made"] = False

        return total

    def reaction_text(reaction_data):

        door_speed_data = reaction_data['door_speed']
        disc_speed_data = reaction_data['disc_speed']
        disc_size_data = reaction_data['disc_size']
        success_data = reaction_data['success']
        fail_data = reaction_data['fail']
        shot_made = reaction_data['last_shot_made']

        if shot_made:
            y_adjustment = int(success_data[-1][-3])
            current_color = list(success_data[-1][-2])

            diff = [abs(color.background[0] - color.success_color[0]),
                    abs(color.background[1] - color.success_color[1]),
                    abs(color.background[2] - color.success_color[2])]

            smallest = min(diff)

            increments = ((diff[0] / smallest),
                          (diff[1] / smallest),
                          (diff[2] / smallest))
        else:
            y_adjustment = int(fail_data[-1][-3])
            current_color = list(fail_data[-1][-2])

            diff = [abs(color.background[0] - color.fail_color[0]),
                    abs(color.background[1] - color.fail_color[1]),
                    abs(color.background[2] - color.fail_color[2])]

            smallest = min(diff)

            increments = ((diff[0] / smallest),
                          (diff[1] / smallest),
                          (diff[2] / smallest))

        if color.background[0] - current_color[0] < 0:
            current_color[0] -= increments[0] * react_fade_speed
        else:
            current_color[0] += increments[0] * react_fade_speed
        if color.background[1] - current_color[1] < 0:
            current_color[1] -= increments[1] * react_fade_speed
        else:
            current_color[1] += increments[1] * react_fade_speed
        if color.background[2] - current_color[2] < 0:
            current_color[2] -= increments[2] * react_fade_speed
        else:
            current_color[2] += increments[2] * react_fade_speed

        current_color = (int(current_color[0]), int(current_color[1]), int(current_color[2]))

        font_style = "darkforest.ttf"
        if success_data:
            success_font_size = 60 - (success_data[-1][2] // 10)
            if success_font_size < 20:
                success_font_size = 20
        else:
            success_font_size = 20

        success_font = pygame.font.Font(f"./{font_style}", int(success_font_size * scaler))
        fail_font = pygame.font.Font(f"./{font_style}", int(20 * scaler))

        directions = [(surface_width // 2, surface_height // 4 + y_adjustment),
                      (surface_width // 2, surface_height - (surface_height // 6) + y_adjustment),
                      (surface_width // 4, surface_height // 2 + y_adjustment),
                      (surface_width - (surface_width // 4), surface_height // 2 + y_adjustment)]

        if not shot_made:
            text_surface = fail_font.render(f"{fail_data[-1][2]}ms", True, current_color)
            text_rect = text_surface.get_rect()

            text_rect.center = directions[fail_data[-1][1] - 1]
            if current_color != color.background:
                surface.blit(text_surface, text_rect)
                reaction_data["fail"][-1][-2] = current_color
            if y_adjustment >= -100:
                reaction_data["fail"][-1][3] -= react_movement_speed

        else:
            text_surface = success_font.render(f"{success_data[-1][2]}ms", True, current_color)
            text_rect = text_surface.get_rect()

            text_rect.center = directions[success_data[-1][0] - 1]
            if current_color != color.background:
                surface.blit(text_surface, text_rect)
                reaction_data["success"][-1][-2] = current_color
            if y_adjustment >= -50:
                reaction_data["success"][-1][3] -= react_movement_speed

        return reaction_data

    def explosion(coords, particles):
        explode_x = coords[0]
        explode_y = coords[-1]
        shrapnel_exists = True
        shrapnel_speed_x = list(range(-50, 50))
        shrapnel_speed_y = list(range(-50, 50))

        for i in range(200):
            explode_speed_x = random.choice(shrapnel_speed_x)
            explode_speed_y = random.choice(shrapnel_speed_y)
            shrapnel_size = random.randint(5, 20)

            particles.append([
                [explode_x, explode_y],
                [explode_speed_x, explode_speed_y],
                shrapnel_size,
                shrapnel_exists
            ])

        return particles

    def anim_explosion(particles, shrapnel_color):
        # index explanation
        # [0][0] [0][1] [explode_x, explode_y],
        # [1][0] [1][1] [explode_speed_x, explode_speed_y],
        # [2] 2 shrapnel_size,
        # [3] 3 shrapnel_exists

        for current_particle in particles:
            current_particle[0][0] += current_particle[1][0]
            current_particle[0][1] += current_particle[1][1]
            current_particle[2] -= random.choice([.1, .3, .5, .7, 1])
            current_particle[1][1] += 2

            pygame.draw.rect(surface, shrapnel_color,
                             (int(current_particle[0][0]),
                              int(current_particle[0][1]),
                              int(current_particle[2]),
                              int(current_particle[2])))

            if current_particle[2] <= 0:
                current_particle[3] = False

        for current_particle in all_particles:
            if not current_particle[3]:
                all_particles.remove(current_particle)
        return particles

    def timer(elapsed_seconds):
        return time_limit - elapsed_seconds

    doors = Doors()
    ball = Ball()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "q":
                    game_over = True

        clock.tick(fps)
        surface.fill(color.background)

        ball_scored, ball_direction, ball_coord = ball.launch()
        time_remaining_decimal = round(timer((pygame.time.get_ticks() - timer_marker) / 1000), 2)  # precise timer
        time_remaining = int(time_remaining_decimal)  # main game timer
        all_particles = anim_explosion(all_particles, disc_explosion_color)
        disc_color_rising, disc_color = ball.ball_pulse(disc_color_rising, disc_color)
        doors.draw_doors()
        draw_margin(margin_color, margin_return_nominal_state)

        #  *note: doors.slide_N returns the following: door_N_x, door_N_y, door_N_y_front_side
        #         [ball_direction - 1]: 0 - un-launched, 1 - top, 2 - bottom, 3 - left, 4 - right
        chosen_door_coords = [doors.slide_T(),
                              doors.slide_B(),
                              doors.slide_L(),
                              doors.slide_R()][ball_direction - 1]

        if not game_over:

            if ball_scored:
                margin_color = color.success_color
                margin_return_nominal_state = 1
                score = ball.score
                react_success = True
                # print(f"1: {ball.start_mark_close, ball_direction} current/last active door: {doors.last_open}")
                current_react_data = build_reaction_data(
                    current_react_data,
                    react_success,
                    ball.start_mark_close,
                    ball_direction,
                    doors.last_open)
            else:
                # created to change index when searching chosen_door_coords for either front side or back side
                if (ball_direction - 1) < 2:
                    x, y = 0, -1
                else:
                    x, y = -1, 1

                collision_result_front, collide_location = ball.collision(
                    ball_coord[0],
                    ball_coord[-1],
                    chosen_door_coords[x],
                    chosen_door_coords[y])

                if not collision_result_front:
                    collision_result_back, collide_location = ball.collision(
                        ball_coord[0],
                        ball_coord[-1],
                        chosen_door_coords[0],
                        chosen_door_coords[1])

                if any([collision_result_front, collision_result_back]):

                    react_success = False
                    # print(f"0: {ball.start_mark_close, ball_direction} current/last active door: {doors.last_open}")
                    current_react_data = build_reaction_data(
                        current_react_data,
                        react_success,
                        ball.start_mark_close,
                        ball_direction,
                        doors.last_open)

                    lives -= 1
                    collisions += 1
                    margin_color = color.fail_color
                    all_particles = explosion(collide_location, all_particles)
                    disc_explosion_color = ball.get_ball_color(current_disc_color)

                    if lives == 0:
                        margin_return_nominal_state = 0
                        doors.locked = True
                        game_over = True

                    else:
                        margin_return_nominal_state = 0
                        ball = Ball()
                        ball.rest = 10
                        ball.score = score

        if time_remaining_decimal < 0:
            margin_return_nominal_state = 0
            doors.locked = True
            game_over = True

        if any([margin_color == color.fail_color, margin_color == color.success_color]):
            margin_return_nominal_state += 1
            if margin_return_nominal_state == margin_return_nominal_state_duration:
                margin_color = color.margin_color
                margin_return_nominal_state = 0

        accuracy_result = accuracy(score, collisions, doors.get_openings())

        if not game_over:

            current_disc_color = ball.draw_ball(disc_color)
            ball.shadow(current_disc_color)
            doors.draw_doors()
            draw_margin(margin_color, margin_return_nominal_state)
            stats(accuracy_result, lives, time_remaining)

        else:
            if len(all_particles) <= 1:
                return game_over, accuracy_result, time_remaining, current_react_data

        if current_react_data:
            current_react_data = reaction_text(current_react_data)

        if score == score_goal:
            return game_over, accuracy_result, time_remaining, current_react_data

        pygame.display.update()
