import pygame
from Smooth.Objects_smooth import Snake, Apple, Surface, Wall, \
    Screen, Bad_Apple, dict_of_not_blocked_buttons


def create_screen(height, width):
    screen = pygame.display.set_mode((height, width))
    return screen


def start_clock():
    clock_ = pygame.time.Clock()
    return clock_


def draw_snake(surface, snake: Snake):
    [(pygame.draw.rect(surface=surface,
                       color=snake.color,
                       rect=(x, y, snake.head_size, snake.head_size))) for x, y in snake.body]


def draw_apple(surface, apple: Apple):
    pygame.draw.rect(surface=surface,
                     color=apple.color,
                     rect=(apple.x, apple.y, apple.size, apple.size))


def draw_surface(surface, surface_: Surface, snake: Snake):
    [pygame.draw.rect(surface=surface,
                      color=surface_.color,
                      rect=(x, y, snake.head_size - 2, snake.head_size - 2))
     for x, y in surface_.body]


def wall_teleport(snake: Snake, height, width):
    if snake.x > width - snake.head_size:
        snake.x = 0
    elif snake.x < 0:
        snake.x = width - snake.head_size
    elif snake.y > height - snake.head_size:
        snake.y = 0
    elif snake.y < 0:
        snake.y = width - snake.head_size


#
def snake_touching(snake: Snake):
    return len(snake.body) != len(set(snake.body))


def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


def draw_wall(walls: Wall, snake: Snake, surface):
    [pygame.draw.rect(surface=surface,
                      color=walls.color,
                      rect=(x, y, snake.head_size - 2, snake.head_size - 2))
     for x, y in walls.wall]


def wall_collision(snake: Snake, wall: Wall):
    return snake.body[-1] in wall.wall


def change_snake_color(*value):
    Snake.color = value[1]


def change_apple_color(*value):
    Apple.color = value[1]


def change_bad_apple_color(*value):
    Bad_Apple.color = value[1]


def change_screen_color(*value):
    Screen.color = value[1]


def change_screen_height(value):
    Screen.height = int(value)


def change_screen_width(value):
    Screen.width = int(value)


def change_speed(value):
    Snake.speed = int(value)


def change_length(value):
    Snake.length = int(value)
