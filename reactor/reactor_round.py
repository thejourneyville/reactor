import pygame
import reactor_colors as color


def round_screen(surface, surface_width, surface_height, margin, margin_color, disc_pulse_value, disc_pulse_direction, scaler, clock, fps):

    round_font_position = 0
    round_font_speed = 500
    round_font_animating = True
    round_font_open_count = 0
    round_number = 1
    score_goal = 15
    timer = 60
    pygame.display.set_caption(f"ROUND {round_number}")
    reactor_start = False
    game_over = False

    def render_text():

        font_style_title = "SF Square Head Bold.ttf"
        font_style_text = "darkforest.ttf"

        round_font = pygame.font.Font(f"./{font_style_title}", int(75 * scaler))
        instructions_font = pygame.font.Font(f"./{font_style_text}", int(30 * scaler))

        round_font_surface = round_font.render(f"ROUND {round_number}", False, color.alert_red)
        instructions_surface = instructions_font.render(
            f"must score {score_goal} points in {timer} seconds", True, color.instructions_color)

        round_font_rect = round_font_surface.get_rect()
        instructions_rect = instructions_surface.get_rect()

        round_font_rect.centerx, round_font_rect.centery = round_font_position, surface_height // 2 - (15 * scaler)
        instructions_rect.centerx, instructions_rect.centery = surface_width // 2, surface_height // 2 + (50 * scaler)

        surface.blit(round_font_surface, round_font_rect)

        if not round_font_animating:

            surface.blit(instructions_surface, instructions_rect)

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

    while not reactor_start:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "s":
                    return game_over

                    round_font_open_count = 0
                    round_font_animating = True

                elif pygame.key.name(event.key) == "q":
                    game_over = True
                    return game_over



        clock.tick(fps)
        surface.fill(color.background)

        draw_margin()
        disc_pulse_value, disc_pulse_direction = draw_background_disc(disc_pulse_value, disc_pulse_direction)
        round_font_animating, round_font_open_count, round_font_position = title_animation(
            round_font_animating, round_font_open_count, round_font_position)
        render_text()

        pygame.display.update()


