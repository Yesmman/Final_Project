from game_functions_smooth import *
from menus_smooth import create_pause_menu


def game():
    pygame.display.set_caption("Snake")

    pygame.init()

    screen = Screen()
    snake = Snake()
    apple = Apple()
    bad_apple = Bad_Apple()
    bad_apple_is_on = False
    snake.length = 1
    score = 0
    surface = create_screen(screen.height, screen.width)
    clock = start_clock()

    snake.first_spawn(screen.height, screen.width)
    apple.spawn(snake, screen.height, screen.width)

    font = pygame.font.SysFont("arial", 20, bold=True)

    menu = create_pause_menu(False)

    game_end = False

    pause = False
    code = 0
    buttons_dict = dict_of_not_blocked_buttons()
    while not game_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pause = not pause
                    if pause:
                        menu = create_pause_menu(True)
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
                code = event.key

        if not pause:

            surface.fill(pygame.Color(screen.color))
            score_text = font.render(f'Score: {score}', True, "orange")
            surface.blit(score_text, (0, 0))
            wall_teleport(snake, screen.height, screen.width)

            draw_apple(surface, apple)
            draw_snake(surface, snake)

            game_end = snake_touching(snake)

            if snake.body[-1] == (apple.x, apple.y):
                snake.eating()
                apple.spawn(snake, screen.height, screen.width)
                score += 1

            if score % 5 == 0 and not bad_apple_is_on:
                if score != 0:
                    bad_apple.spawn(snake, screen.height, screen.width)
                    if (bad_apple.x, bad_apple.y) == (apple.x, apple.y):
                        bad_apple.spawn(snake, screen.height, screen.width)
                    bad_apple_is_on = True

            if bad_apple_is_on:
                draw_apple(surface, bad_apple)
                if snake.body[-1] == (bad_apple.x, bad_apple.y):
                    score -= 7
                    bad_apple_is_on = False
            if score < 0:
                game_end = True
            buttons_dict = snake.moving(buttons_dict, code)

            pygame.display.flip()
            clock.tick(snake.speed)
