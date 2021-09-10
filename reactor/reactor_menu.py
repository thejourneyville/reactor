import pygame
import reactor_main_game
import reactor_round as round_screen
import reactor_colors as color
import reactor_account_create as create

# initializing pygame
pygame.init()

# screen/surface setup:
width, height = 1, 1  # screen aspect ratio
display_info_object = pygame.display.Info()
screen_width, screen_height = display_info_object.current_w, display_info_object.current_h
screen_scaler = height / screen_height
scaler = 1
surface_width, surface_height = int((width / screen_scaler) * scaler), int((height / screen_scaler) * scaler)
surface = pygame.display.set_mode((surface_width, surface_height))

# window caption, clock speed
pygame.display.set_caption("REACTOR MENU")
clock = pygame.time.Clock()
fps = 60

# margin thickness, color
margin = int(60 * scaler)
margin_color = color.margin_color

# music
# pygame.mixer.music.load("tron_sample.mp3")
# pygame.mixer.music.play(-1)

def start_menu():

    # variables
    accuracy, timer = 0, 0
    title_position = 0
    title_speed = 500
    title_animating = True
    title_open_count = 0
    blinker_on = True
    blinker_count = 0
    blinker_speed = 10
    disc_pulse_value = 0
    disc_pulse_direction = True

    def render_text():

        # note: 'timer' is not currently being rendered but it is being passed from the game, so it could be added

        if accuracy or timer:  # initially set to 0, these variables returned after game is played as tuples
            shot_accuracy = accuracy[0]
            total_openings = accuracy[-1]
        else:
            shot_accuracy = 0
            total_openings = 0

        font_style_title = "SF Square Head Bold.ttf"
        font_style_text = "darkforest.ttf"

        title = pygame.font.Font(f"./{font_style_title}", int(150 * scaler))
        start_font = pygame.font.Font(f"./{font_style_text}", int(60 * scaler))
        instructions_font = pygame.font.Font(f"./{font_style_text}", int(30 * scaler))
        stats_font = pygame.font.Font(f"./{font_style_text}", int(40 * scaler))

        title_surface = title.render("REACT0R", False, color.title_color)
        start_surface = start_font.render("press [enter]", True, color.start_color)
        instructions_surface = instructions_font.render(
            "using arrow keys, launch the disc through the open doors", True, color.instructions_color)
        shot_accuracy_surface = stats_font.render(f"shots made/total: {shot_accuracy} pct.", True, color.stats_color)
        total_openings_surface = stats_font.render(f"tries/openings: {total_openings} pct.", True, color.stats_color)

        title_rect = title_surface.get_rect()
        start_rect = start_surface.get_rect()
        instructions_rect = instructions_surface.get_rect()
        shot_accuracy_rect = shot_accuracy_surface.get_rect()
        total_openings_rect = total_openings_surface.get_rect()

        title_rect.centerx, title_rect.centery = title_position, surface_height // 4 + (100 * scaler)
        start_rect.centerx, start_rect.centery = surface_width // 2, (surface_height // 2) + (35 * scaler)
        instructions_rect.centerx, instructions_rect.centery = surface_width // 2, surface_height // 2 - (50 * scaler)
        shot_accuracy_rect.centerx, shot_accuracy_rect.centery = \
            surface_width // 2, surface_height - surface_height // 2 + (130 * scaler)
        total_openings_rect.centerx, total_openings_rect.centery = \
            surface_width // 2, surface_height - surface_height // 2 + (160 * scaler)

        surface.blit(title_surface, title_rect)

        if not title_animating:

            surface.blit(instructions_surface, instructions_rect)

            if blinker_on:
                surface.blit(start_surface, start_rect)

            if accuracy or timer:
                surface.blit(shot_accuracy_surface, shot_accuracy_rect)
                surface.blit(total_openings_surface, total_openings_rect)

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

    def start_text_blinker(count, status):

        count += 1
        if count == blinker_speed:
            count = 0
            if status:
                status = False
            else:
                status = True

        return count, status

    def title_animation(title_start, count, position):

        if title_start:
            position += title_speed
            position = position % (surface_width * 2)
            count += 1
            if count == 25:
                title_start = False
                position = (surface_width // 2) % (surface_width * 2)  # for title_rect.centerx

        return title_start, count, position

    def draw_margin():

        pygame.draw.rect(surface, margin_color, (0, 0, surface_width, surface_height), margin)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    # create account
                    user_account = create.account_create(surface, surface_width, surface_height, margin, margin_color,
                                                         disc_pulse_value, disc_pulse_direction,
                                                         scaler, clock, fps)
                    if user_account:
                        print(user_account)

                    accuracy, timer = round_screen.level_screen(surface, surface_width, surface_height,
                                                                margin, margin_color,
                                                                disc_pulse_value, disc_pulse_direction,
                                                                scaler, clock, fps, user_account)

                    # accuracy, timer = reactor_main_game.run_reactor(
                    #     surface, surface_width, surface_height, margin, margin_color, disc_pulse_value, disc_pulse_direction, scaler, clock, fps)
                    pygame.display.set_caption("REACTOR MENU")
                    title_open_count = 0
                    title_animating = True

                elif pygame.key.name(event.key) == "q":
                    quit()

                elif pygame.key.name(event.key) == "r":
                    title_open_count = 0
                    accuracy, timer = 0, 0
                    title_animating = True

        clock.tick(fps)
        surface.fill(color.background)

        draw_margin()
        disc_pulse_value, disc_pulse_direction = draw_background_disc(disc_pulse_value, disc_pulse_direction)
        title_animating, title_open_count, title_position = title_animation(
            title_animating, title_open_count, title_position)
        blinker_count, blinker_on = start_text_blinker(blinker_count, blinker_on)
        render_text()

        pygame.display.update()


if __name__ == "__main__":
    start_menu()
