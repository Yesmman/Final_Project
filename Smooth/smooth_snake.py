from game_functions_smooth import *
from menus_smooth import create_pause_menu


def game():
    pygame.display.set_caption("Snake")
    mode = Mode()
    pygame.init()

    screen = Screen()
    snake = Snake()
    apple = Apple()
    bad_apple = Bad_Apple()

    wall = Wall()

    bad_apple_is_on = False

    snake.length = 1

    score = 0

    surface = create_screen(screen.height, screen.width)

    clock = start_clock()

    font = pygame.font.SysFont(name="arial",
                               size=20,
                               bold=True)

    menu = create_pause_menu(False)

    game_end = False

    pause = False

    buttons_dict = dict_of_not_blocked_buttons()

    wall_is_enable = False

    if mode.mode == "Side wall on":
        wall_is_enable = True
        wall.generate_side_walls(snake, screen.width, screen.width)

    if mode.mode == "Side wall off":
        wall_is_enable = False
    print(wall.wall)
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

            # game_end = snake_touching(snake)

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

            buttons_dict = snake.moving(buttons_dict)
            surface.blit(score_text, (0, 0))
            pygame.display.flip()
            clock.tick(snake.speed)
