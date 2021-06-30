from game_functions_smooth import *
from menus_smooth import create_pause_menu


def single_game():
    pygame.display.set_caption("Snake: 1 player")
    pygame.init()

    mode = Mode()
    screen = Screen()
    snake = Snake()
    apple = Apple()
    bad_apple = Bad_Apple()

    wall = Wall()

    bad_apple_is_on = False

    score = 0

    surface = create_screen(screen.height, screen.width)

    clock = start_clock()

    font = pygame.font.SysFont(name="arial",
                               size=20,
                               bold=True)

    menu = create_pause_menu(False)

    game_end = False

    pause = False

    wall_is_enable = False

    if mode.mode == "Side wall on":
        wall_is_enable = True
        wall.generate_side_walls(snake, screen.width, screen.width)

    if mode.mode == "Side wall off":
        wall_is_enable = False

    buttons = dict_key_to_buttons()
    buttons_dict = dict_of_not_blocked_buttons()

    snake.first_spawn(screen.height, screen.width, wall_is_enable)
    apple.spawn(snake, screen.height, screen.width, wall_is_enable)

    while not game_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pause = not pause
                    if pause:
                        menu = create_pause_menu(on=True)
                    if not menu.is_enabled():
                        pause = False
                if event.key == pygame.K_t:
                    snake.body[-1] = snake.body[-2]
                if event.key == pygame.K_l:
                    snake.body[-1] = (apple.x, apple.y)
                if event.key == pygame.K_u:
                    snake.speed += 10
                if event.key == pygame.K_i:
                    snake.speed -= 10
                if event.key == pygame.K_o:
                    snake.length -= 5

        if not pause:

            surface.fill(pygame.Color(screen.color))
            score_text = font.render(f'Score: {score}', True, "orange")

            if wall_is_enable:
                game_end = wall_collision(snake=snake, wall=wall) or snake_touching(snake)
                draw_wall(surface=surface,
                          walls=wall,
                          snake=snake)

            else:
                wall_teleport(snake, screen.height, screen.width)
                game_end = snake_touching(snake)
            draw_apple(surface, apple)
            draw_snake(surface, snake)

            if snake.body[-1] == (apple.x, apple.y):
                snake.eating()
                apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                score += 1

            if score % 5 == 0 and not bad_apple_is_on:
                if score != 0:
                    bad_apple.spawn(snake, screen.height, screen.width)
                    if (bad_apple.x, bad_apple.y) == (apple.x, apple.y):
                        bad_apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                    bad_apple_is_on = True

            if bad_apple_is_on:
                draw_apple(surface, bad_apple)
                if snake.body[-1] == (bad_apple.x, bad_apple.y):
                    score -= 7
                    bad_apple_is_on = False

            if score < 0:
                game_end = True

            buttons_dict = snake.moving(buttons, buttons_dict)
            buttons = dict2_key_to_buttons()
            surface.blit(score_text, (0, 0))
            pygame.display.flip()
            clock.tick(snake.speed)


def two_players():
    pygame.display.set_caption("Snake: 2 players")
    pygame.init()

    mode = Mode()
    screen = Screen()

    snake = Snake()
    snake_2 = Second_Snake()

    apple = Apple()
    bad_apple = Bad_Apple()
    wall = Wall()

    bad_apple_is_on = False

    score = 0
    score_2 = 0

    surface = create_screen(screen.height, screen.width)

    clock = start_clock()

    font = pygame.font.SysFont(name="arial",
                               size=20,
                               bold=True)

    menu = create_pause_menu(False)

    game_end_1 = False
    game_end_2 = False

    pause = False

    wall_is_enable = False

    if mode.mode == "Side wall on":
        wall_is_enable = True
        wall.generate_side_walls(snake, screen.width, screen.width)

    if mode.mode == "Side wall off":
        wall_is_enable = False

    buttons = dict_key_to_buttons()
    second_buttons = dict2_of_not_blocked_buttons()
    start_pause = True
    buttons_dict = dict_of_not_blocked_buttons()
    second_buttons_dict = dict2_of_not_blocked_buttons()

    snake.first_spawn(screen.height, screen.width, wall_is_enable)
    snake_2.first_spawn(screen.height, screen.width, wall_is_enable)

    def collision(tuple_1, tuple_2):
        return tuple_1 == tuple_2

    if collision(snake_2, snake):
        snake_2.first_spawn(screen.height, screen.width, wall_is_enable)

    apple.spawn(snake, screen.height, screen.width, wall_is_enable)

    if collision((apple.x, apple.y), snake_2):
        apple.spawn(snake, screen.height, screen.width, wall_is_enable)

    while not game_end_1 or not game_end_2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                start_pause = False
                if event.key == pygame.K_r:
                    pause = not pause
                    if pause:
                        menu = create_pause_menu(on=True)
                    if not menu.is_enabled():
                        pause = False
                if event.key == pygame.K_t:
                    snake.body[-1] = snake.body[-2]
                if event.key == pygame.K_l:
                    snake.body[-1] = (apple.x, apple.y)
                if event.key == pygame.K_u:
                    snake.speed += 10
                if event.key == pygame.K_i:
                    snake.speed -= 10
                if event.key == pygame.K_o:
                    snake.length -= 5
                if event.key == pygame.K_z:
                    two_players()
                    return

        if not pause:

            surface.fill(pygame.Color(screen.color))
            score_text = font.render(f'Score: {score}', True, "orange")
            score_text_2 = font.render(f'Score: {score_2}', True, "blue")
            if wall_is_enable:
                if not game_end_1:
                    game_end_1 = wall_collision(snake=snake, wall=wall) or snake_touching(snake) or snake_collision(
                        snake, snake_2)
                if not game_end_2:
                    game_end_2 = wall_collision(snake_2, wall) or snake_touching(snake_2) or snake_collision(snake_2,
                                                                                                             snake)
                draw_wall(surface=surface,
                          walls=wall,
                          snake=snake)
            else:
                wall_teleport(snake, screen.height, screen.width)
                wall_teleport(snake_2, screen.height, screen.width)
                if not game_end_1:
                    game_end_1 = snake_touching(snake) or snake_collision(snake, snake_2)
                if not game_end_2:
                    game_end_2 = snake_touching(snake_2) or snake_collision(snake_2, snake)

            draw_apple(surface, apple)

            if not game_end_1:
                draw_snake(surface, snake)
            else:
                snake.body.clear()
                snake.body.append((-10, -10))

            if not game_end_2:
                draw_snake(surface, snake_2)
            else:
                snake_2.body.clear()
                snake_2.body.append((-5, -5))

            if snake.body[-1] == (apple.x, apple.y):
                snake.eating()
                apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                score += 1

            if snake_2.body[-1] == (apple.x, apple.y):
                snake_2.eating()
                apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                while collision((apple.x, apple.y), snake_2):
                    apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                score_2 += 1

            if (score % 5 == 0 or score_2 % 5 == 0) and not bad_apple_is_on:
                if score != 0:
                    bad_apple.spawn(snake, screen.height, screen.width)
                    if (bad_apple.x, bad_apple.y) == (apple.x, apple.y):
                        bad_apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                    bad_apple_is_on = True

            if bad_apple_is_on:
                draw_apple(surface, bad_apple)

            if snake.body[-1] == (bad_apple.x, bad_apple.y):
                score -= 7
                bad_apple_is_on = False

            if snake_2.body[-1] == (bad_apple.x, bad_apple.y):
                score_2 -= 7
                bad_apple_is_on = False
            if score_2 < 0:
                game_end_2 = True
            if score < 0:
                game_end_1 = True

            if not game_end_1:
                buttons_dict = snake.moving(buttons, buttons_dict)
            if not game_end_2:
                second_buttons_dict = snake_2.moving(second_buttons, second_buttons_dict)

            buttons = dict_key_to_buttons()
            second_buttons = dict2_key_to_buttons()

            surface.blit(score_text, (0, 0))
            surface.blit(score_text_2, (0, screen.width - snake.head_size))

            pygame.display.flip()
            while start_pause:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        start_pause = False
            clock.tick(snake.speed)
