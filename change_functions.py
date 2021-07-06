from Objects_smooth import Snake, Screen, Mode, Net


def change_color(obj: type, *value):
    obj.color = value[1]


def change_screen_height(value):
    Screen.height = int(value)


def change_screen_width(value):
    Screen.width = int(value)


def change_speed(value):
    Snake.speed = int(value)


def change_length(value):
    Snake.length = int(value)


def change_mode(attribute, *value):
    setattr(Mode, attribute, value[1])


def change_net_host(value):
    Net.host = value


def change_net_port(value):
    Net.port = int(value)
