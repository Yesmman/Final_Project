from random import randrange

import pygame


class Snake:
    color = "green"
    speed = 20
    head_size = 20

    def __init__(self):
        self.score = 0

        self.x = 0
        self.y = 0
        self.length = 1
        self.body = []

        self.step_x = 0
        self.step_y = 0

        self.buttons_dict = {}

    def moving(self, buttons, not_blocked_button: dict):
        self.body.append((self.x, self.y))
        self.body = self.body[-self.length:]

        x = not_blocked_button

        if enable_moving(self):
            if buttons["w"] and not_blocked_button["w"]:
                self.step_x, self.step_y = dicts.dict_steps["w"]
                x = block_button(self, "s")

            if buttons["s"] and not_blocked_button["s"]:
                self.step_x, self.step_y = dicts.dict_steps["s"]
                x = block_button(self, "w")

            if buttons["d"] and not_blocked_button["d"]:
                self.step_x, self.step_y = dicts.dict_steps["d"]
                x = block_button(self, "a")

            if buttons["a"] and not_blocked_button["a"]:
                self.step_x, self.step_y = dicts.dict_steps["a"]
                x = block_button(self, "d")
        self.x += self.step_x * round(self.head_size ** (1 / 2))
        self.y += self.step_y * round(self.head_size ** (1 / 2))

        return x

    def eating(self):

        self.length += 5
        Snake.speed += 2
        self.speed += 2
        self.score += 1

    def first_spawn(self, height, width, wall=False):

        self.body.clear()
        self.x = randrange(0, width, self.head_size)
        self.y = randrange(0, height, self.head_size)
        self.body.append((self.x, self.y))
        if wall:
            if self.body[-1] in Wall.wall:
                self.first_spawn(height, width, True)


class Second_Snake(Snake):
    color = "pink"


class Apple:
    x = -100
    y = -100

    color = "red"

    size = 20

    def spawn(self, snake: Snake, height, width, wall=False):

        self.x = randrange(0, width, snake.head_size)
        self.y = randrange(0, height, snake.head_size)
        if (self.x, self.y) in snake.body:
            self.spawn(snake, height, width)
        if wall:
            if (self.x, self.y) in Wall.wall:
                self.spawn(snake, height, width, True)


class Bad_Apple(Apple):
    color = "blue"


class Wall:
    color = "brown"
    x = 0
    y = 0
    wall = [(x, y)]

    def generate_side_walls(self, snake: Snake, height, width):
        self.x = 0
        self.y = 0
        self.wall.clear()
        self.wall.append((self.x, self.y))

        while snake.head_size + self.x <= width:
            self.x += snake.head_size
            self.wall.append((self.x, self.y))
            self.wall.append((self.y, self.x))

        while snake.head_size + self.y <= height:
            self.y += snake.head_size
            self.wall.append((self.x - snake.head_size, self.y))
            self.wall.append((self.y, self.x - snake.head_size))


class Mode:
    mode = "Side wall off"
    player = "One"


class Screen:
    height = 500
    width = 500
    color = "black"


class Online_snake(Snake):
    color = "yellow"
    speed = 20


class Net:
    host = '127.0.0.1'
    port = 65432


def wasd_keys():
    key = pygame.key.get_pressed()
    dict_of_buttons = {
        "w": key[dicts.second["Up"]],
        "s": key[dicts.second["Down"]],
        "a": key[dicts.second["Left"]],
        "d": key[dicts.second["Right"]],
    }
    return dict_of_buttons


def block_button(obj: Snake, button):
    dictionary = {
        "w": True,
        "s": True,
        "d": True,
        "a": True,

    }
    if obj.length != 1:
        dictionary[button] = False
    return dictionary


def dict_of_not_blocked_buttons():
    dictionary = {
        "w": True,
        "s": True,
        "d": True,
        "a": True,
    }
    return dictionary


def dict2_of_not_blocked_buttons():
    dictionary = {
        "w": True,
        "s": True,
        "d": True,
        "a": True,
    }
    return dictionary


def numpad_keys():
    key = pygame.key.get_pressed()
    dict_of_buttons = {
        "w": key[dicts.first["Up"]],
        "s": key[dicts.first["Down"]],
        "a": key[dicts.first["Left"]],
        "d": key[dicts.first["Right"]],
    }
    return dict_of_buttons


def enable_moving(snake):
    return snake.body[-1][0] % snake.head_size == 0 and snake.body[-1][1] % snake.head_size == 0


class dicts:
    dict_steps = {
        "w": (0, -1),
        "s": (0, 1),
        "d": (1, 0),
        "a": (-1, 0),
    }
    first = {
        "Up": pygame.K_KP5,
        "Down": pygame.K_KP2,
        "Left": pygame.K_KP1,
        "Right": pygame.K_KP3,
    }
    second = {
        "Up": pygame.K_w,
        "Down": pygame.K_s,
        "Left": pygame.K_a,
        "Right": pygame.K_d,
    }
