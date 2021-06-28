import pygame
from random import randrange


def game():
    game_end = False

    def create_apple():
        created_apple = randrange(0, height_screen, head_size), randrange(0, height_screen, head_size)
        return created_apple

    def draw_snake():
        [(pygame.draw.rect(screen, pygame.Color("green"), (i, j, head_size - 10, head_size - 10))) for i, j in snake]

    def draw_apple():
        pygame.draw.rect(screen, pygame.Color("red"), (apple[0], apple[1], head_size - 10, head_size - 10))

    def eating_apple():
        if snake[-1][0] >= apple[0]:
            check_1 = snake[-1][0] - apple[0] < head_size
        else:
            check_1 = apple[0] - snake[-1][0] < head_size
        if snake[-1][1] >= apple[1]:
            check_2 = snake[-1][1] - apple[1] < head_size
        else:
            check_2 = apple[1] - snake[-1][1] < head_size
        return check_2 and check_1

    height_screen = 500
    width_screen = 500
    head_size = 25
    pygame.init()

    screen = pygame.display.set_mode((height_screen, width_screen))
    pygame.display.set_caption("Snake")

    clock = pygame.time.Clock()

    x = randrange(0, height_screen, head_size)
    y = randrange(0, height_screen, head_size)
    snake = [(x, y)]
    snake_length = 1
    dx, dy = 0, 0
    speed = 40

    running = True
    apple = create_apple()

    score = 0
    score_text = pygame.font.SysFont('Arial', 25, bold=True)

    game_over = pygame.font.SysFont('Arial', 25, bold=True)
    current_buttons = {
        'W': True,
        'S': True,
        'A': True,
        'D': True
    }
    while running:
        key = pygame.key.get_pressed()
        screen.fill(pygame.Color("black"))

        draw_snake()
        draw_apple()

        score_output = score_text.render(f'Score: {score}', True, pygame.Color("Blue"))
        screen.blit(score_output, (0, 0))
        snake.append((x, y))
        snake = snake[-snake_length:]

        if eating_apple():
            snake_length += 10
            speed += 3
            score += 1
            apple = create_apple()
            if apple in snake:
                create_apple()

        pygame.display.flip()
        clock.tick(speed)

        if len(snake) != len(set(snake)):
            game_end = True
        if game_end:
            game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        if key[pygame.K_w] and current_buttons['W']:
            dx, dy = 0, -1
            current_buttons = {
                'W': True,
                'S': False,
                'A': True,
                'D': True
            }

        if key[pygame.K_s] and current_buttons['S']:
            dx, dy = 0, 1
            current_buttons = {
                'W': False,
                'S': True,
                'A': True,
                'D': True
            }

        if key[pygame.K_d] and current_buttons['D']:
            dx, dy = 1, 0
            current_buttons = {
                'W': True,
                'S': True,
                'A': False,
                'D': True
            }

        if key[pygame.K_a] and current_buttons['A']:
            dx, dy = -1, 0
            current_buttons = {
                'W': True,
                'S': True,
                'A': True,
                'D': False
            }
        x += dx * head_size / 10
        y += dy * head_size / 10
        if x > width_screen - head_size:
            x = 0
            draw_snake()
        elif x < 0:
            x = width_screen - head_size
            draw_snake()
        elif y > width_screen - head_size:
            y = 0
            draw_snake()
        elif y < 0:
            y = width_screen - head_size
            draw_snake()


game()
