import pygame

# initializing pygame
pygame.init()

# screen/surface setup:
width, height = 1, 1  # screen aspect ratio
display_info_object = pygame.display.Info()
screen_width, screen_height = display_info_object.current_w, display_info_object.current_h
screen_scaler = height / screen_height
scaler = .5
surface_width, surface_height = int((width / screen_scaler) * scaler), int((height / screen_scaler) * scaler)
surface = pygame.display.set_mode((surface_width, surface_height))

# window caption, clock speed
pygame.display.set_caption("FLOATING WINDOW TEST")
clock = pygame.time.Clock()
fps = 120


def move_box(x, y):
    pygame.draw.rect(surface,
                     (255, 255, 255),
                     (x - diff_x, y - diff_y,
                      square, square),
                     1
                     )
    return x - diff_x, y - diff_y


def draw_box(x, y):
    pygame.draw.rect(surface,
                     (255, 255, 255),
                     (x, y,
                      square, square),
                     5
                     )


def text(x, y):
    style = "darkforest.ttf"

    font_center = pygame.font.Font(f"./{style}", square // 3)
    position_center = (x + square // 2, y + square // 2)
    surf = (font_center.render(f"TEXT", True, (255, 255, 255)))
    rect = surf.get_rect()
    rect.center = position_center
    surface.blit(surf, rect)


square = int(300 * scaler)
box_x, box_y = (surface_width // 2) - 50, (surface_height // 2) - 50
measured = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    clock.tick(fps)
    surface.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()

    if box_x - 5 <= mx <= box_x + square + 5 and box_y - 5 <= my <= box_y + square + 5:

        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
            if not measured:
                diff_x, diff_y = abs(box_x - mx), abs(box_y - my)
                measured = True

            box_x, box_y = move_box(mx, my)
            text(box_x, box_y)

            if box_x + square > surface_width:
                box_x = surface_width - square

            if box_x < 0:
                box_x = 0

            if box_y + square > surface_height:
                box_y = surface_height - square

            if box_y < 0:
                box_y = 0

        else:
            measured = False
            draw_box(box_x, box_y)
            text(box_x, box_y)
    else:
        draw_box(box_x, box_y)
        text(box_x, box_y)

    pygame.display.update()
