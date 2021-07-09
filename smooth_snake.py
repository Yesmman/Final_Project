from game_functions_smooth import *
from menus_smooth import create_pause_menu
import socket
import pickle

import threading


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

    surface = create_screen(screen.height, screen.width)

    clock = start_clock()

    font = pygame.font.SysFont(name="arial",
                               size=20,
                               bold=True)

    menu = create_pause_menu(on=False)

    game_end = False

    pause = False

    wall_is_enable = False

    if mode.mode == "Side wall on":
        wall_is_enable = True
        wall.generate_side_walls(snake, screen.width, screen.width)

    if mode.mode == "Side wall off":
        wall_is_enable = False

    buttons = wasd_keys()
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
                if event.key == pygame.K_u:
                    snake.speed += 10
                if event.key == pygame.K_i:
                    snake.speed -= 10

        if not pause:

            surface.fill(pygame.Color(screen.color))
            score_text = font.render(f'Score: {snake.score}', True, "orange")

            if wall_is_enable:
                game_end = wall_collision(snake=snake, wall=wall) or \
                           snake_touching(snake) or \
                           snake.score < 0
                draw_wall(surface=surface,
                          walls=wall,
                          snake=snake)
            else:
                wall_teleport(snake, screen.height, screen.width)
                game_end = snake_touching(snake) or \
                           snake.score < 0

            draw_apple(surface, apple)
            draw_snake(surface, snake)

            if snake.body[-1] == (apple.x, apple.y):
                snake.eating()
                apple.spawn(snake, screen.height, screen.width, wall_is_enable)

            if snake.score % 5 == 0 and not bad_apple_is_on:
                if snake.score:
                    bad_apple.spawn(snake, screen.height, screen.width)
                    if (bad_apple.x, bad_apple.y) == (apple.x, apple.y):
                        bad_apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                    bad_apple_is_on = True

            if bad_apple_is_on:
                draw_apple(surface, bad_apple)
                if snake.body[-1] == (bad_apple.x, bad_apple.y):
                    snake.score -= 7
                    bad_apple_is_on = False

            buttons_dict = snake.moving(buttons, buttons_dict)
            buttons = numpad_keys()

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

    surface = create_screen(height=screen.height,
                            width=screen.width)

    clock = start_clock()

    font = pygame.font.SysFont(name="arial",
                               size=20,
                               bold=True)

    menu = create_pause_menu(on=False)

    game_end_1 = False
    game_end_2 = False

    pause = False

    wall_is_enable = False

    if mode.mode == "Side wall on":
        wall_is_enable = True
        wall.generate_side_walls(snake, screen.width, screen.width)

    if mode.mode == "Side wall off":
        wall_is_enable = False
    start_pause = True

    buttons = wasd_keys()
    second_buttons = numpad_keys()

    snake.buttons_dict = dict_of_not_blocked_buttons()
    snake_2.buttons_dict = dict2_of_not_blocked_buttons()

    snake.first_spawn(screen.height, screen.width, wall_is_enable)
    snake_2.first_spawn(screen.height, screen.width, wall_is_enable)

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
                if event.key == pygame.K_u:
                    snake.speed += 10
                if event.key == pygame.K_i:
                    snake.speed -= 10
                if event.key == pygame.K_z:
                    two_players()
                    return

        if not pause:

            surface.fill(pygame.Color(screen.color))
            score_text = font.render(f'Score: {snake.score}', True, "orange")
            score_text_2 = font.render(f'Score: {snake_2.score}', True, "blue")
            if wall_is_enable:
                if not game_end_1:
                    game_end_1 = wall_collision(snake=snake, wall=wall) or \
                                 snake_touching(snake) or \
                                 snake_collision(snake, snake_2) or \
                                 snake.score < 0
                if not game_end_2:
                    game_end_2 = wall_collision(snake_2, wall) or \
                                 snake_touching(snake_2) or \
                                 snake_collision(snake_2, snake) or \
                                 snake_2.score

                draw_wall(surface=surface,
                          walls=wall,
                          snake=snake)
            else:
                wall_teleport(snake, screen.height, screen.width)
                wall_teleport(snake_2, screen.height, screen.width)
                if not game_end_1:
                    game_end_1 = snake_touching(snake) or \
                                 snake_collision(snake, snake_2) or \
                                 snake.score < 0
                if not game_end_2:
                    game_end_2 = snake_touching(snake_2) or \
                                 snake_collision(snake_2, snake) or \
                                 snake_2.score < 0

            draw_apple(surface, apple)

            if not game_end_1:
                draw_snake(surface, snake)
            else:
                snake.body.clear()
                snake.body.append((-50, -50))

            if not game_end_2:
                draw_snake(surface, snake_2)
            else:
                snake_2.body.clear()
                snake_2.body.append((-30, -30))

            if snake.body[-1] == (apple.x, apple.y):
                snake.eating()
                apple.spawn(snake, screen.height, screen.width, wall_is_enable)

            if snake_2.body[-1] == (apple.x, apple.y):
                snake_2.eating()
                apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                while collision((apple.x, apple.y), snake_2):
                    apple.spawn(snake, screen.height, screen.width, wall_is_enable)

            if (snake.score % 5 == 0 or snake_2.score % 5 == 0) and not bad_apple_is_on:
                if snake.score and snake_2.score:
                    bad_apple.spawn(snake, screen.height, screen.width)
                    if (bad_apple.x, bad_apple.y) == (apple.x, apple.y):
                        bad_apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                    bad_apple_is_on = True

            if bad_apple_is_on:
                draw_apple(surface, bad_apple)

            if snake.body[-1] == (bad_apple.x, bad_apple.y):
                snake.score -= 7
                bad_apple_is_on = False

            if snake_2.body[-1] == (bad_apple.x, bad_apple.y):
                snake_2.score -= 7
                bad_apple_is_on = False

            if not game_end_1:
                snake.buttons_dict = snake.moving(buttons, snake.buttons_dict)
            if not game_end_2:
                snake_2.buttons_dict = snake_2.moving(second_buttons, snake_2.buttons_dict)

            buttons = wasd_keys()
            second_buttons = numpad_keys()

            surface.blit(score_text, (0, 0))
            surface.blit(score_text_2, (0, screen.width - snake.head_size))

            pygame.display.flip()
            while start_pause:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        start_pause = False
            clock.tick(max(snake.speed, snake_2.speed))


def online_two_players():
    pygame.display.set_caption("Snake: 2 players, online")
    pygame.init()

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(('', 0))

    server = Net.host, Net.port

    mode = Mode()
    screen = Screen()

    snake = Snake()
    snake_2 = Online_snake()

    apple = Apple()
    bad_apple = Bad_Apple()
    wall = Wall()

    bad_apple_is_on = False

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
    start_pause = True

    buttons = wasd_keys()

    snake.buttons_dict = dict_of_not_blocked_buttons()

    snake.first_spawn(screen.height, screen.width, wall_is_enable)

    def get_online_snake():
        while True:
            try:
                data = client.recv(1024)
                pickled_data = pickle.loads(data)
                snake_2.body = pickled_data["Snake"]
                apple.x = pickled_data["Apple"][0]
                apple.y = pickled_data["Apple"][1]

                snake_2.score = pickled_data["Score"]
            except ConnectionResetError:
                pass

    thread = threading.Thread(target=get_online_snake, daemon=True)

    if collision(snake_2, snake):
        snake.first_spawn(screen.height, screen.width, wall_is_enable)

    thread.start()

    dict_of_data = {}

    apple_is_eaten = False
    while not game_end_1 or not game_end_2:
        dict_of_data.clear()

        dict_of_data["Snake"] = snake.body
        dict_of_data["Is eaten"] = apple_is_eaten
        dict_of_data["Score"] = snake.score

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
                if event.key == pygame.K_u:
                    snake.speed += 10
                if event.key == pygame.K_i:
                    snake.speed -= 10
                if event.key == pygame.K_z:
                    online_two_players()
                    return

        if not pause:

            client.sendto((pickle.dumps(dict_of_data)), server)
            apple_is_eaten = False

            surface.fill(pygame.Color(screen.color))
            score_text = font.render(f'Score: {snake.score}', True, "orange")
            score_text_2 = font.render(f'Score: {snake_2.score}', True, "blue")

            if wall_is_enable:
                if not game_end_1:
                    game_end_1 = wall_collision(snake=snake, wall=wall) or \
                                 snake_touching(snake) or \
                                 snake_collision(snake, snake_2) or \
                                 snake.score < 0

                draw_wall(surface=surface,
                          walls=wall,
                          snake=snake)
            else:
                wall_teleport(snake, screen.height, screen.width)
                if not game_end_1:
                    game_end_1 = snake_touching(snake) or \
                                 snake_collision(snake, snake_2) or \
                                 snake.score < 0

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
                apple_is_eaten = True

            if snake.score % 5 == 0 and not bad_apple_is_on:
                if snake.score != 0:
                    bad_apple.spawn(snake, screen.height, screen.width)
                    if (bad_apple.x, bad_apple.y) == (apple.x, apple.y):
                        bad_apple.spawn(snake, screen.height, screen.width, wall_is_enable)
                    bad_apple_is_on = True

            if bad_apple_is_on:
                draw_apple(surface, bad_apple)

            if snake.body[-1] == (bad_apple.x, bad_apple.y):
                snake.score -= 7
                bad_apple_is_on = False

            if not game_end_1:
                snake.buttons_dict = snake.moving(buttons, snake.buttons_dict)

            buttons = wasd_keys()

            surface.blit(score_text, (0, 0))
            surface.blit(score_text_2, (0, screen.width - snake.head_size))

            pygame.display.flip()
            while start_pause:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        start_pause = False
            clock.tick(max(snake.speed, snake_2.speed))
