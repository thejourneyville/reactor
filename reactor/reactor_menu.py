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
darkgrey = (100, 100, 100)
red = (240, 17, 59)
yellow = (255, 169, 0)
orange = (255, 118, 0)
purple = (82, 0, 106)

margin = 25
margin_color = purple

# music
pygame.mixer.music.load("tron_sample.mp3")
pygame.mixer.music.play(-1)

accuracy, time = 0, 0


def stats(accuracy, timer):

    font_style = "darkforest.ttf"
    font = pygame.font.Font(f"./{font_style}", int(40 * scaler))
    title = pygame.font.Font(f"./{font_style}", int(250 * scaler))
    text_color = black

    title_surface = title.render("REACTOR", True, text_color)
    title_rect = title_surface.get_rect()
    title_rect.centerx, title_rect.centery = surface_width // 2, surface_height // 4
    surface.blit(title_surface, title_rect)

    start_surface = font.render("press [s]tart to begin", True, text_color)
    start_rect = start_surface.get_rect()
    start_rect.centerx, start_rect.centery = surface_width // 2, surface_height // 2
    surface.blit(start_surface, start_rect)

    if accuracy or timer != 0:
        shot_accuracy = accuracy[0]
        total_openings = accuracy[-1]

        text_surface1 = font.render(f"shots made/total: {shot_accuracy} pct.", True, text_color)
        # text_surface2 = font.render(str(timer), True, text_color)
        text_surface3 = font.render(f"tries/openings: {total_openings} pct.", True, text_color)

        text_rect1 = text_surface1.get_rect()
        # text_rect2 = text_surface2.get_rect()
        text_rect3 = text_surface3.get_rect()

        text_rect1.centerx, text_rect1.centery = surface_width // 2, surface_height - surface_height // 4
        # text_rect2.centerx, text_rect2.centery = surface_width // 2, surface_height - surface_height // 4 + 40 * scaler
        text_rect3.centerx, text_rect3.centery = surface_width // 2, surface_height - surface_height // 4 + 80 * scaler

        surface.blit(text_surface1, text_rect1)
        # surface.blit(text_surface2, text_rect2)
        surface.blit(text_surface3, text_rect3)


while True:

    clock.tick(fps)
    surface.fill(lightgrey)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "s":
                accuracy, time = reactor_main_game.run_reactor(surface, surface_width, surface_height, scaler, clock, fps)

            elif pygame.key.name(event.key) == "q":
                quit()

    pygame.display.set_caption("REACTOR MENU")
    rendered_margin = pygame.draw.rect(surface, margin_color, (0, 0, surface_width, surface_height), margin)
    stats(accuracy, time)

    pygame.display.update()

