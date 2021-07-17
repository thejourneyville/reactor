import pygame
import reactor_main_game

# initializing pygame
pygame.init()

# screen/surface setup:
phone_w, phone_h = 1, 1  # screen aspect ratio
display_info_object = pygame.display.Info()
screen_width, screen_height = display_info_object.current_w, display_info_object.current_h
screen_scaler = phone_h / screen_height
scaler = .75
surface_width, surface_height = int((phone_w / screen_scaler) * scaler), int((phone_h / screen_scaler) * scaler)
surface = pygame.display.set_mode((surface_width, surface_height))

# window caption, clock speed
pygame.display.set_caption("REACTOR MENU")
clock = pygame.time.Clock()
fps = 60

# colors
white = (255, 255, 255)
black = (0, 0, 0)
lightgrey = (150, 150, 150)
darkgrey = (140, 140, 140)
red = (200, 17, 59)
yellow = (255, 169, 0)
orange = (255, 118, 0)
purple = (82, 0, 106)

margin = 25
margin_color = purple

# music
pygame.mixer.music.load("tron_sample.mp3")
pygame.mixer.music.play(-1)

accuracy, time = 0, 0
title_pos = 0
speed = 500
title_open = True
title_open_count = 0
blinker = True
blinker_count = 0
blinker_speed = 20


def stats(accuracy, timer, title_position, on_off):

    font_style = "darkforest.ttf"
    font = pygame.font.Font(f"./{font_style}", int(40 * scaler))
    instructions_font = pygame.font.Font(f"./{font_style}", int(30 * scaler))
    title = pygame.font.Font(f"./{font_style}", int(250 * scaler))
    text_color = black

    title_surface = title.render("REACTOR", True, text_color)
    title_rect = title_surface.get_rect()
    title_rect.centerx, title_rect.centery = title_position, surface_height // 4
    surface.blit(title_surface, title_rect)

    if on_off:
        start_surface = font.render("press [s]tart to begin", True, red)
        start_rect = start_surface.get_rect()
        start_rect.centerx, start_rect.centery = surface_width // 2, surface_height // 2
        surface.blit(start_surface, start_rect)

    if accuracy or timer != 0:
        shot_accuracy = accuracy[0]
        total_openings = accuracy[-1]

        text_surface1 = instructions_font.render(f"shots made/total: {shot_accuracy} pct.", True, text_color)
        # text_surface2 = font.render(str(timer), True, text_color)
        text_surface3 = instructions_font.render(f"tries/openings: {total_openings} pct.", True, text_color)

        text_rect1 = text_surface1.get_rect()
        # text_rect2 = text_surface2.get_rect()
        text_rect3 = text_surface3.get_rect()

        text_rect1.centerx, text_rect1.centery = surface_width // 2, surface_height - surface_height // 2 + (80 * scaler)
        # text_rect2.centerx, text_rect2.centery = surface_width // 2, surface_height - surface_height // 4 + 40 * scaler
        text_rect3.centerx, text_rect3.centery = surface_width // 2, surface_height - surface_height // 2 + (110 * scaler)

        surface.blit(text_surface1, text_rect1)
        # surface.blit(text_surface2, text_rect2)
        surface.blit(text_surface3, text_rect3)

    else:
        instructions_surface = instructions_font.render(
            "using arrow keys, launch the disc through the open doors", True, text_color)
        instructions_rect = instructions_surface.get_rect()
        instructions_rect.centerx, instructions_rect.centery = surface_width // 2, surface_height // 2 - (50 * scaler)
        surface.blit(instructions_surface, instructions_rect)


def draw_ball():
    pygame.draw.circle(
        surface,
        darkgrey,
        (surface_width // 2, surface_height // 2),
        surface_width // 2 * scaler,
        int(75 * scaler))


while True:

    clock.tick(fps)
    surface.fill(lightgrey)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "s":
                accuracy, time = reactor_main_game.run_reactor(surface, surface_width, surface_height, scaler, clock, fps)
                title_open_count = 0
                title_open = True

            elif pygame.key.name(event.key) == "q":
                quit()

            elif pygame.key.name(event.key) == "r":
                title_open_count = 0
                title_open = True

    pygame.display.set_caption("REACTOR MENU")

    if title_open:
        title_pos += speed
        current_title_pos = title_pos % (surface_width * 2)
        title_open_count += 1
        if title_open_count == 25:
            title_open = False
            title_pos = surface_width // 2
    else:
        current_title_pos = title_pos % (surface_width * 2)

    if blinker:
        blinker_count += 1
        if blinker_count == blinker_speed:
            blinker_count = 0
            blinker = False

    else:
        blinker_count += 1
        if blinker_count == blinker_speed:
            blinker_count = 0
            blinker = True

    draw_ball()

    stats(accuracy, time, current_title_pos, blinker)
    rendered_margin = pygame.draw.rect(surface, margin_color, (0, 0, surface_width, surface_height), margin)


    pygame.display.update()

