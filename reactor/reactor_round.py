import pygame
import reactor_colors as color
import reactor_main_game as main


def round_screen(surface, surface_width, surface_height, margin, margin_color,
                 disc_pulse_value, disc_pulse_direction,
                 scaler, clock, fps):
    round_font_position = 0
    round_font_speed = 500
    round_font_animating = True
    round_font_open_count = 0
    round_number = 1
    score_goal = 15
    timer = 60
    pygame.display.set_caption(f"ROUND {round_number}")
    door_speed = 15
    round_screen_loop = True
    accuracy_result, time_remaining = 0, 0

    def render_text():

        font_style_title = "SF Square Head Bold.ttf"
        font_style_text = "darkforest.ttf"
        font_style_speed = "darkforest.ttf"

        round_font = pygame.font.Font(f"./{font_style_title}", int(75 * scaler))
        instructions_font = pygame.font.Font(f"./{font_style_text}", int(30 * scaler))
        speed_font = pygame.font.Font(f"./{font_style_speed}", int(30 * scaler))

        round_font_surface = round_font.render(f"ROUND {round_number}", True, color.instructions_color)
        instructions_surface = instructions_font.render(
            f"must score {score_goal} points in {timer} seconds", True, color.instructions_color)
        speed_font_surface = speed_font.render(f"reactor speed {door_speed}", True, color.alert_red)

        round_font_rect = round_font_surface.get_rect()
        instructions_rect = instructions_surface.get_rect()
        speed_font_rect = speed_font_surface.get_rect()

        round_font_rect.centerx, round_font_rect.centery = round_font_position, surface_height // 2 - (30 * scaler)
        instructions_rect.centerx, instructions_rect.centery = surface_width // 2, surface_height // 2 + (60 * scaler)
        speed_font_rect.center = (surface_width // 2, surface_height // 2 + (20 * scaler))

        surface.blit(round_font_surface, round_font_rect)

        if not round_font_animating:
            surface.blit(instructions_surface, instructions_rect)
            surface.blit(speed_font_surface, speed_font_rect)

    def draw_background_disc(dissolve, disc_pulse_up):

        if disc_pulse_up:
            dissolve += 1
        else:
            dissolve -= 2

        if dissolve <= 0:
            disc_pulse_up = True
        elif dissolve >= 50:
            disc_pulse_up = False

        pygame.draw.circle(
            surface,
            (color.background[0] - int(dissolve),
             color.background[1] - int(dissolve),
             color.background[2] - int(dissolve)),
            (surface_width // 2, surface_height // 2),
            (surface_width // 2) - margin,
            int(100 * scaler))

        return dissolve, disc_pulse_up

    def title_animation(title_start, count, position):

        if title_start:
            position += round_font_speed
            position = position % (surface_width * 2)
            count += 1
            if count == 25:
                title_start = False
                position = (surface_width // 2) % (surface_width * 2)  # for title_rect.centerx

        return title_start, count, position

    def draw_margin():

        pygame.draw.rect(surface, margin_color, (0, 0, surface_width, surface_height), margin)

    while round_screen_loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "s":
                    game_over, accuracy_result, time_remaining, current_react_data = main.run_reactor(surface,
                                                                                                      surface_width,
                                                                                                      surface_height,
                                                                                                      margin,
                                                                                                      margin_color,
                                                                                                      scaler, clock,
                                                                                                      fps, door_speed,
                                                                                                      score_goal)
                    if game_over:
                        return accuracy_result, time_remaining
                    print(accuracy_result)
                    print(current_react_data)

                elif pygame.key.name(event.key) == "q":
                    return accuracy_result, time_remaining

        clock.tick(fps)
        surface.fill(color.background)

        draw_margin()
        disc_pulse_value, disc_pulse_direction = draw_background_disc(disc_pulse_value, disc_pulse_direction)
        round_font_animating, round_font_open_count, round_font_position = title_animation(
            round_font_animating, round_font_open_count, round_font_position)
        render_text()

        pygame.display.update()
