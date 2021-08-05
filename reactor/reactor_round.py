import pygame
import reactor_colors as color
import reactor_main_game as main
import reactor_stats as stats


def level_screen(surface, surface_width, surface_height, margin, margin_color,
                 disc_pulse_value, disc_pulse_direction,
                 scaler, clock, fps):
    level_font_position = 0
    level_font_speed = 500
    level_font_animating = True
    level_font_open_count = 0
    level = 1
    score_goal = 60
    time_limit = 150
    pygame.display.set_caption(f"LEVEL {level}")
    door_speed = 23
    level_screen_loop = True
    accuracy_result, time_remaining = 0, 0

    def render_text():

        font_style_title = "SF Square Head Bold.ttf"
        font_style_text = "darkforest.ttf"
        font_style_speed = "darkforest.ttf"

        level_font = pygame.font.Font(f"./{font_style_title}", int(75 * scaler))
        instructions_font = pygame.font.Font(f"./{font_style_text}", int(30 * scaler))
        speed_font = pygame.font.Font(f"./{font_style_speed}", int(30 * scaler))

        level_font_surface = level_font.render(f"LEVEL {level}", True, color.instructions_color)
        instructions_surface = instructions_font.render(
            f"must score {score_goal} points in {time_limit} seconds", True, color.instructions_color)
        speed_font_surface = speed_font.render(f"reactor speed {door_speed}", True, color.alert_red)

        level_font_rect = level_font_surface.get_rect()
        instructions_rect = instructions_surface.get_rect()
        speed_font_rect = speed_font_surface.get_rect()

        level_font_rect.centerx, level_font_rect.centery = level_font_position, surface_height // 2 - (30 * scaler)
        instructions_rect.centerx, instructions_rect.centery = surface_width // 2, surface_height // 2 + (60 * scaler)
        speed_font_rect.center = (surface_width // 2, surface_height // 2 + (20 * scaler))

        surface.blit(level_font_surface, level_font_rect)

        if not level_font_animating:
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
            position += level_font_speed
            position = position % (surface_width * 2)
            count += 1
            if count == 25:
                title_start = False
                position = (surface_width // 2) % (surface_width * 2)  # for title_rect.centerx

        return title_start, count, position

    def draw_margin():

        pygame.draw.rect(surface, margin_color, (0, 0, surface_width, surface_height), margin)

    while level_screen_loop:

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
                                                                                                      score_goal,
                                                                                                      time_limit)
                    # for testing
                    # print(f"accuracy_result: {accuracy_result}")
                    # print(f"current_react_data: {current_react_data}")
                    # print(f"time remaining: {time_remaining}")
                    time_elapsed = time_limit - time_remaining

                    stats.stats(surface, surface_width, surface_height, margin_color,
                                scaler, clock, fps, level, current_react_data, time_elapsed)

                    if game_over:
                        return accuracy_result, time_remaining

                elif pygame.key.name(event.key) == "q":
                    return accuracy_result, time_remaining

        clock.tick(fps)
        surface.fill(color.background)

        draw_margin()
        disc_pulse_value, disc_pulse_direction = draw_background_disc(disc_pulse_value, disc_pulse_direction)
        level_font_animating, level_font_open_count, level_font_position = title_animation(
            level_font_animating, level_font_open_count, level_font_position)
        render_text()

        pygame.display.update()