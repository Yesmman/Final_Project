from random import randrange

import pygame


class Snake:
    length = 1
    x: int
    y: int

    body = []

    head_size = 25
    color = "green"
    speed = 20

    step_x = 0
    step_y = 0

    def moving(self, not_blocked_button: dict):

        self.body.append((self.x, self.y))
        self.body = self.body[-self.length:]
        buttons = dict_key_to_buttons()
        x = not_blocked_button
        if enable_moving(self):

            if buttons["w"] and not_blocked_button["w"]:
                self.step_x = 0
                self.step_y = -1
                x = block_button(self, "s")

            if buttons["s"] and not_blocked_button["s"]:
                self.step_x = 0
                self.step_y = 1
                x = block_button(self, "w")

            if buttons["d"] and not_blocked_button["d"]:
                self.step_x = 1
                self.step_y = 0
                x = block_button(self, "a")

            if buttons["a"] and not_blocked_button["a"]:
                self.step_x = -1
                self.step_y = 0
                x = block_button(self, "d")
        self.x += self.step_x * 5
        self.y += self.step_y * 5
        # print(x)
        return x

    def eating(self):

        self.length += 5

        self.speed += 1

    def first_spawn(self, height, width, wall=False):

        self.body.clear()
        self.x = randrange(0, width, self.head_size)
        self.y = randrange(0, height, self.head_size)
        self.body.append((self.x, self.y))
        if wall:
            if self.body[-1] in Wall.wall:
                self.first_spawn(height, width, True)

    def __repr__(self):
        return str(self.body)


class Apple:
    x = 0
    y = 0

    color = "red"

    size = 25

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

    def __repr__(self):
        return self.mode


class Screen:
    height = 500
    width = 500
    color = "black"


def dict_key_to_buttons():
    key = pygame.key.get_pressed()
    dict_of_buttons = {
        "w": key[pygame.K_w],
        "s": key[pygame.K_s],
        "a": key[pygame.K_a],
        "d": key[pygame.K_d],
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


#
# def dict_buttons_to_steps():
#     dictionary = {
#         "w": (0, -1),
#         "s": (0, 1),
#         "d": (1, 0),
#         "a": (-1, 0),
#     }
#     return dictionary


def enable_moving(snake: Snake):
    return snake.body[-1][0] % snake.head_size == 0 and snake.body[-1][1] % snake.head_size == 0
