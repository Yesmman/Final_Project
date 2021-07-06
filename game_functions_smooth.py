
from Objects_smooth import *


def create_screen(height, width):
    screen = pygame.display.set_mode((height, width))
    return screen


def start_clock():
    clock_ = pygame.time.Clock()
    return clock_


def draw_snake(surface, snake: Snake):
    # pygame.time.wait(int(1000/snake.speed))
    [(pygame.draw.rect(surface=surface,
                       color=snake.color,
                       rect=(x, y, snake.head_size, snake.head_size))) for x, y in snake.body]


def draw_apple(surface, apple: Apple):
    pygame.draw.rect(surface=surface,
                     color=apple.color,
                     rect=(apple.x, apple.y, apple.size, apple.size))


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
def snake_touching(snake):
    return len(snake.body) != len(set(snake.body))


def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


def draw_wall(walls: Wall, snake: Snake, surface):
    [pygame.draw.rect(surface=surface,
                      color=walls.color,
                      rect=(x, y, snake.head_size, snake.head_size))
     for x, y in walls.wall]


def wall_collision(snake: Snake, wall: Wall):
    return snake.body[-1] in wall.wall


def snake_collision(snake, snake_2):
    return snake.body[-1] in snake_2.body

