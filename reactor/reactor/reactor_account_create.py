import pygame
import reactor_colors as color


def account_create(surface, surface_width, surface_height, margin, margin_color,
                 disc_pulse_value, disc_pulse_direction,
                 scaler, clock, fps):

    blinker_on = True
    blinker_count = 0
    blinker_speed = 3
    user_account = "benny"

    def draw_background_disc(dissolve, disc_pulse_up):

        if disc_pulse_up:
            dissolve += .5
        else:
            dissolve -= .5

        if dissolve <= 0:
            disc_pulse_up = True
        elif dissolve >= 25:
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

    def draw_margin():

        pygame.draw.rect(surface, margin_color, (0, 0, surface_width, surface_height), margin)

    def mouse_coord():
        mx, my = pygame.mouse.get_pos()
        return mx, my

    def text_board():

        row_space = 50 * scaler
        board_text = "darkforest.ttf"

        instructions = pygame.font.Font(f"./{board_text}", int(30 * scaler))
        alphabet = pygame.font.Font(f"./{board_text}", int(50 * scaler))

        instructions_text = "please enter your account name"
        keyboard_1 = "q w e r t y u i o p"
        keyboard_2 = "a s d f g h j k l"
        keyboard_3 = "z x c v b n m"
        keyboard_4 = "adv rub end"

        biggest_let = "m"
        biggest_let_rect = alphabet.render(biggest_let, True, color.title_color).get_rect()
        let_x_size = abs(biggest_let_rect.left - biggest_let_rect.right)
        let_y_size = abs(biggest_let_rect.top - biggest_let_rect.bottom)

        row1_x_start = (surface_width - (len(keyboard_1) * let_x_size)) // 2
        row2_x_start = (surface_width - (len(keyboard_2) * let_x_size)) // 2
        row3_x_start = (surface_width - (len(keyboard_3) * let_x_size)) // 2
        row4_x_start = (surface_width - (len(keyboard_4) * let_x_size)) // 2

        instructions_surface = instructions.render(instructions_text, True, color.title_color)
        alphabet_1_surfaces = [alphabet.render(let, True, color.title_color) for let in keyboard_1]
        alphabet_2_surfaces = [alphabet.render(let, True, color.title_color) for let in keyboard_2]
        alphabet_3_surfaces = [alphabet.render(let, True, color.title_color) for let in keyboard_3]
        alphabet_4_surfaces = [alphabet.render(let, True, color.title_color) for let in keyboard_4]

        instructions_rect = instructions_surface.get_rect()
        alphabet_1_rects = [surf.get_rect() for surf in alphabet_1_surfaces]
        alphabet_2_rects = [surf.get_rect() for surf in alphabet_2_surfaces]
        alphabet_3_rects = [surf.get_rect() for surf in alphabet_3_surfaces]
        alphabet_4_rects = [surf.get_rect() for surf in alphabet_4_surfaces]

        instructions_rect_pos = (instructions_position, surface_height // 4 + row_space)

        alphabet_1_rects_pos = [(row1_x_start + (let_x_size * idx), surface_height // 4 + row_space * 2)
                                for idx, rect in enumerate(alphabet_1_rects)]
        alphabet_2_rects_pos = [(row2_x_start + (let_x_size * idx), surface_height // 4 + row_space * 3) for idx, rect
                                in enumerate(alphabet_2_rects)]
        alphabet_3_rects_pos = [(row3_x_start + (let_x_size * idx), surface_height // 4 + row_space * 4) for idx, rect
                                in enumerate(alphabet_3_rects)]
        alphabet_4_rects_pos = [(row4_x_start + (let_x_size * idx), surface_height // 4 + row_space * 5) for idx, rect
                                in enumerate(alphabet_4_rects)]

        all_keyboard_pos = alphabet_1_rects_pos + alphabet_2_rects_pos + alphabet_3_rects_pos + alphabet_4_rects_pos

        instructions_rect.center = instructions_rect_pos
        surface.blit(instructions_surface, instructions_rect)
        if not instructions_font_animating:
            for idx, pos in enumerate(alphabet_1_rects_pos):
                alphabet_1_rects[idx].topleft = pos
                surface.blit(alphabet_1_surfaces[idx], alphabet_1_rects[idx])
            for idx, pos in enumerate(alphabet_2_rects_pos):
                alphabet_2_rects[idx].topleft = pos
                surface.blit(alphabet_2_surfaces[idx], alphabet_2_rects[idx])
            for idx, pos in enumerate(alphabet_3_rects_pos):
                alphabet_3_rects[idx].topleft = pos
                surface.blit(alphabet_3_surfaces[idx], alphabet_3_rects[idx])
            for idx, pos in enumerate(alphabet_4_rects_pos):
                alphabet_4_rects[idx].topleft = pos
                surface.blit(alphabet_4_surfaces[idx], alphabet_4_rects[idx])

        return all_keyboard_pos, (let_x_size, let_y_size)

    def highlight_text(coord, k_pos, letter):

        x = coord[0]
        y = coord[1]
        letters = "q w e r t y u i o pa s d f g h j k lz x c v b n madv rub end"
        highlighted, highlighted_pos = None, None
        output_letter = None

        for idx, pos in enumerate(k_pos):

            if idx < 49:  # 0 - 48 represents all letters and spaces between them
                if pos[0] <= x < pos[0] + letter[0]:
                    if pos[-1] <= y < pos[-1] + letter[-1]:
                        if letters[idx] != " ":
                            highlighted, highlighted_pos = idx, pos
                            output_letter = idx

            elif idx >= 49:
                if pos[0] <= x < pos[0] + letter[0]:
                    if pos[-1] <= y < pos[-1] + letter[-1]:
                        if letters[idx] != " ":
                            if 49 <= idx <= 51:
                                highlighted, highlighted_pos = [49, 50, 51], [k_pos[49], k_pos[50], k_pos[51]]
                                output_letter = 49
                            elif 53 <= idx <= 55:
                                highlighted, highlighted_pos = [53, 54, 55], [k_pos[53], k_pos[54], k_pos[55]]
                                output_letter = 53
                            elif 57 <= idx <= 59:
                                highlighted, highlighted_pos = [57, 58, 59], [k_pos[57], k_pos[58], k_pos[59]]
                                output_letter = 57

        if highlighted is not None and highlighted_pos is not None:

            board_text = "darkforest.ttf"
            alphabet = pygame.font.Font(f"./{board_text}", int(50 * scaler))

            if not instructions_font_animating:
                if isinstance(highlighted, int):
                    hovered_let_surface = alphabet.render(letters[highlighted], True, color.alert_red, color.background)
                    hovered_let_rect = hovered_let_surface.get_rect()
                    hovered_let_rect.topleft = highlighted_pos
                    surface.blit(hovered_let_surface, hovered_let_rect)

                else:
                    for l_idx, idx in enumerate(highlighted):
                        hovered_let_surface = alphabet.render(letters[idx], True, color.alert_red, color.background)
                        hovered_let_rect = hovered_let_surface.get_rect()
                        hovered_let_rect.topleft = highlighted_pos[l_idx]
                        surface.blit(hovered_let_surface, hovered_let_rect)

        return output_letter

    def print_name(timer, command, user_name, key_positions, letter_size, keyboard):

        name_complete = False
        letters = "q w e r t y u i o pa s d f g h j k lz x c v b n madv rub end"
        if command == 49:
            action = "adv"
        elif command == 53:
            action = "rub"
        elif command == 57:
            action = "end"
        elif command is None:
            pass
        else:
            action = letters[command]

        if command is not None:
            if not keyboard:
                if command < 49:
                    if timer >= 10:
                        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                            timer = 0
                            if timer == 0:
                                if len(user_name) < 12:
                                    user_name += letters[command]

                elif command == 49:
                    if timer >= 10:
                        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                            timer = 0
                            if timer == 0:
                                if len(user_name) < 12:
                                    user_name += "_"
                elif command == 53:
                    if timer >= 10:
                        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                            timer = 0
                            if timer == 0:
                                user_name = user_name[:-1]
                elif command == 57:
                    if timer >= 10:
                        if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                            timer = 0
                            if timer == 0:
                                name_complete = True
                                return timer, user_name, name_complete

            else:
                if command < 49:
                    timer = 0
                    if timer == 0:
                        if len(user_name) < 12:
                            user_name += letters[command]
                elif command == 49:
                    timer = 0
                    if timer == 0:
                        if len(user_name) < 12:
                            user_name += "_"
                elif command == 53:
                    timer = 0
                    if timer == 0:
                        user_name = user_name[:-1]
                elif command == 57:
                    timer = 0
                    if timer == 0:
                        name_complete = True
                        return timer, user_name, name_complete

        timer += 1

        board_text = "SF Square Head Bold.ttf"
        name_text = pygame.font.Font(f"./{board_text}", int(70 * scaler))

        row_x_start = (surface_width // 2)
        name_surface = name_text.render(user_name, True, color.sky_blue)
        name_rect = name_surface.get_rect()
        name_rect_pos = (row_x_start, surface_height - surface_height // 3)
        name_rect.center = name_rect_pos
        surface.blit(name_surface, name_rect)

        return timer, user_name, name_complete

    def instructions_animation(title_start, count, position):

        if title_start:
            position += instructions_font_speed
            position = position % (surface_width * 2)
            count += 1
            if count == 25:
                title_start = False
                position = (surface_width // 2) % (surface_width * 2)

        return title_start, count, position

    instructions_position = 0
    instructions_font_speed = 500 * scaler
    instructions_font_animating = True
    instructions_font_open_count = 0

    keys = [pygame.K_q, " ", pygame.K_w, " ", pygame.K_e, " ", pygame.K_r, " ", pygame.K_t, " ", pygame.K_y, " ",
            pygame.K_u, " ", pygame.K_i, " ", pygame.K_o, " ", pygame.K_p, pygame.K_a, " ", pygame.K_s, " ", pygame.K_d,
            " ", pygame.K_f, " ", pygame.K_g, " ", pygame.K_h, " ", pygame.K_j, " ", pygame.K_k, " ", pygame.K_l,
            pygame.K_z, " ", pygame.K_x, " ", pygame.K_c, " ", pygame.K_v, " ", pygame.K_b, " ", pygame.K_n, " ",
            pygame.K_m, pygame.K_SPACE, " ", " ", " ", pygame.K_BACKSPACE, " ", " ", " ", pygame.K_RETURN]
    keyboard_pressed = False

    mouse_timer = 0
    account_name = ""
    complete = False
    while not complete:

        surface.fill(color.background)

        draw_margin()
        disc_pulse_value, disc_pulse_direction = draw_background_disc(disc_pulse_value, disc_pulse_direction)

        instructions_font_animating, instructions_font_open_count, instructions_position = \
            instructions_animation(instructions_font_animating, instructions_font_open_count, instructions_position)

        blinker_count, blinker_on = start_text_blinker(blinker_count, blinker_on)

        all_pos, let_size = text_board()
        mouse_xy = mouse_coord()
        hovered_letter = highlight_text(mouse_xy, all_pos, let_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    complete = True
                for idx, pressed in enumerate(keys):
                    if event.key == keys[idx]:
                        keyboard_pressed = True
                        hovered_letter = idx

        mouse_timer, account_name, complete = \
            print_name(mouse_timer, hovered_letter, account_name, all_pos, let_size, keyboard_pressed)
        keyboard_pressed = False

        pygame.display.update()

    if not account_name:
        account_name = "default"
    return account_name

