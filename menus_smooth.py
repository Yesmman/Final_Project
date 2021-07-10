import pygame_menu
import pygame
from functools import partial
from pygame_menu.examples import create_example_window

from pygame_menu.locals import ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT

from change_functions import *

from Objects_smooth import Snake, Screen, Apple, Bad_Apple, Mode, Wall, Second_Snake, Net, Online_snake, dicts

from server import start_server

import pygame
import threading


def main_menu():
    surface = create_example_window(title="Menu",
                                    window_size=(Screen.height, Screen.width))

    menu = pygame_menu.Menu(
        height=400,
        width=400,
        title="Main menu"
    )

    menu.add.button("Play", play)
    menu.add.button("Settings", partial(to_settings,
                                        menu=menu,
                                        surface=surface,
                                        main=True))

    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(surface)
    return menu


def create_pause_menu(on):
    menu = pygame_menu.Menu(
        height=200,
        width=200,
        title="Paused"
    )
    if on:
        surface = create_example_window(title="Menu",
                                        window_size=(Screen.height, Screen.width))

        menu.add.button("Continue", menu.disable)

        menu.add.button("Settings", partial(to_settings,
                                            menu=menu,
                                            surface=surface,
                                            main=False))

        menu.add.button("Help", partial(to_help_menu,
                                        menu=menu,
                                        surface=surface,
                                        main=False))

        menu.add.button("Quit", main_menu)

        menu.mainloop(surface)
    return menu


def to_settings(menu, surface, main):
    menu.close()
    menu.disable()

    settings(surface, main)


def settings(surface, main):
    menu = pygame_menu.Menu(
        height=400,
        width=400,
        title="Settings"
    )
    menu.add.button("Color", partial(to_color_settings,
                                     menu=menu,
                                     surface=surface,
                                     main=main))

    menu.add.button("Controls", partial(to_controls,
                                        menu=menu,
                                        surface=surface,
                                        main=main))

    network_settings = menu.add.button("Network", partial(to_network,
                                                          menu=menu,
                                                          surface=surface,
                                                          main=main))
    network_settings.hide()

    if Mode.player == "Online":
        network_settings.show()

    if main:
        menu.add.button("Back", partial(from_settings_to_main_menu,
                                        menu=menu))
    else:
        menu.add.button("Back", partial(from_settings_to_pause_menu,
                                        menu=menu))

    menu.mainloop(surface)


def to_network(menu, surface, main):
    menu.close()
    menu.disable()

    network(surface, main)


def network(surface, main):
    menu = pygame_menu.Menu(
        height=400,
        width=400,
        title="Network"
    )

    host = menu.add.text_input("Host: ",
                               default=Net.host)
    port = menu.add.text_input("Port: ",
                               default=Net.port)

    cant_start_server_label = menu.add.label("You can't start this server")
    cant_start_server_label.hide()

    def commit():
        host_get = host.get_value()
        port_get = port.get_value()
        change_net_host(host_get)
        change_net_port(port_get)

    menu.add.button("Commit", commit)

    menu.add.button("Back", partial(to_settings,
                                    menu=menu,
                                    surface=surface,
                                    main=main))

    thread = threading.Thread(target=start_server, daemon=True)

    def server_on():
        cant_start_server_label.hide()
        try:
            thread.start()

        except RuntimeError:
            cant_start_server_label.show()

    menu.add.button("Start server", server_on)
    menu.mainloop(surface)


def from_settings_to_main_menu(menu):
    menu.close()
    menu.disable()

    main_menu()


def from_settings_to_pause_menu(menu):
    menu.close()
    menu.disable()

    create_pause_menu(True)


def play():
    from smooth_snake import single_game, two_players, online_two_players

    if Mode.player == "Two":
        two_players()
    elif Mode.player == "One":
        single_game()
    elif Mode.player == "Online":
        online_two_players()


def to_help_menu(menu, surface, main):
    menu.close()
    menu.disable()

    help_menu(surface, main)


def help_menu(surface, main):
    menu = pygame_menu.Menu(
        height=500,
        width=500,
        title="Help"
    )

    dict_of_names = {
        "Snake color": Snake.color,
        "Apple color": Apple.color,
        "Bad apple color": Bad_Apple.color,
        "Second snake color": Second_Snake.color,
        "Online snake color": Online_snake.color,
        "Wall color": Wall.color
    }

    rect = pygame.rect.Rect(0, -12, 25, 25)

    for key in dict_of_names.keys():
        label = menu.add.label(key, align=ALIGN_LEFT, font_size=20, margin=[40, 20])
        dec = label.get_decorator()
        dec.add_rect(-label.get_width() / 2 - 25, 0, rect, color=dict_of_names[key])

    controls_keys = {"WASD": "First player",
                     "Nums:1, 2, 3, 5": "Second/Single player",
                     "R": "game pause (pause menu)",
                     "Z": "restart",
                     "1": "speed up",
                     "2": "speed down"}
    explaining = ["Игра продолжается, пока не погибнут все змейки.",

                  "'Плохое' яблоко появляется каждые 5 очков.",

                  "При поедании плохого яблока снимается 7 очков.",

                  "Игра окончена, если змейка столкнулась со стеной/другой змейкой"
                  ""
                  " или если количество очков меньше 0.",

                  "Побеждает тот, у кого большее количество очков/заполнили максимум экрана"]

    f1 = menu.add.frame_v(150, 100, align=ALIGN_LEFT).relax()
    f2 = menu.add.frame_v(20, 100).relax()
    f3 = menu.add.frame_h(f1.get_width() + f2.get_width(), 300, align=ALIGN_LEFT).relax()

    for items in controls_keys.keys():
        label = menu.add.label(items, font_size=20)
        f1.pack(label)
        label2 = menu.add.label(controls_keys[items], font_size=20)
        f2.pack(label2, )

    f3.pack(f1, align=ALIGN_CENTER)
    f3.pack(f2, align=ALIGN_CENTER)

    f4 = menu.add.frame_v(150, 400, align=ALIGN_LEFT).relax()

    for items in explaining:
        label = menu.add.label(items, font_size=20, max_char=-1)
        f4.pack(label)

    menu.add.button('Back', partial(from_settings_to_pause_menu, menu=menu))

    menu.mainloop(surface)


def to_color_settings(menu, surface, main):
    menu.close()
    menu.disable()

    color(surface, main)


def color(surface, main):
    menu = pygame_menu.Menu(
        height=400,
        width=400,
        title="Color",
    )
    list_of_colors = [
        ("Green", "green"),
        ("Blue", "blue"),
        ("Red", "red"),
        ("Yellow", "yellow"),
        ("Brown", 'brown'),
        ("White", "white"),
        ("Pink", "pink"),
        ("Black", "black"),
        ("Purple", "purple")
    ]
    classes = {
        "Snake color: ": Snake,
        "Apple color: ": Apple,
        "Bad apple color: ": Bad_Apple,
        "Second snake color: ": Second_Snake,
        "Online snake color: ": Online_snake,
        "Wall color: ": Wall,
        "Background color: ": Screen,

    }

    for key in classes:
        menu.add.selector(title=key,
                          default=list_of_colors.index((classes[key].color.title(), classes[key].color)),
                          items=list_of_colors,
                          onchange=partial(change_color, classes[key]),
                          font_size=25)

    menu.add.button("Back", partial(to_settings,
                                    menu=menu,
                                    surface=surface,
                                    main=main))

    menu.mainloop(surface)


def to_controls(menu, surface, main):
    menu.close()
    menu.disable()

    controls(surface, main)


def controls(surface, main):
    menu = pygame_menu.Menu(
        height=500,
        width=500,
        title="Controls",
    )

    label = menu.add.label("Please, input number")
    label_done = menu.add.label("Done!")

    def get_value(button, func):
        value = button.get_value()

        label.hide()
        label_done.hide()

        try:
            func(value)
        except ValueError:
            label.show()
        else:
            label_done.show()

    list_of_buttons_atr = [
        ("Speed: ", Snake.speed),
        ("Height: ", Screen.height),
        ("Width: ", Screen.width),
    ]

    list_of_functions = [change_speed, change_screen_height, change_screen_width]
    list_of_buttons = []

    for buttons in list_of_buttons_atr:
        list_of_buttons.append(menu.add.text_input(buttons[0], buttons[1]))

    label.hide()
    label_done.hide()

    list_of_modes = [
        ("Side wall", "Side wall on"),
        ("Without side walls", "Side wall off")
    ]
    menu.add.selector("Wall mode",
                      default=1,
                      items=list_of_modes,
                      onchange=partial(change_mode, "mode"))

    list_num_of_players = [
        ("Single player", "One"),
        ("Two players", "Two"),
        ("Online", "Online")
    ]

    menu.add.selector("Players: ",
                      default=1,
                      items=list_num_of_players,
                      onchange=partial(change_mode, "player"))

    def commit():
        for index in range(len(list_of_buttons)):
            get_value(button=list_of_buttons[index],
                      func=list_of_functions[index])

    menu.add.button("Commit", commit)

    menu.add.button("Keys", partial(to_keys,
                                    menu=menu,
                                    surface=surface,
                                    main=main))
    menu.add.button("Back", partial(to_settings,
                                    menu=menu,
                                    surface=surface,
                                    main=main))

    menu.mainloop(surface)


def to_keys(menu, surface, main):
    menu.close()
    menu.disable()

    keys(surface, main)


def keys(surface, main):
    menu = pygame_menu.Menu(
        height=500,
        width=500,
        title="Keys",
    )

    menu.add.label("First player")

    def change_key(dict_, text):
        name = ""

        while name != "return":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    code = event.key
                    name = pygame.key.name(code)
                    if name != "return":
                        dict_[text] = code
        menu.close()
        menu.disable()
        keys(surface, main)

    def show_controls(on_dict):
        for items in on_dict.items():
            x = menu.add.label(items[0], font_size=20)
            y = menu.add.button(pygame.key.name(items[1]),
                                font_size=20,
                                action=partial(change_key, on_dict, x.get_title()))
            f = menu.add.frame_h(200, 40).relax()
            f.pack(x)
            f.pack(y, align=ALIGN_RIGHT)

    show_controls(dicts.first)

    menu.add.label("Second player")
    show_controls(dicts.second)
    menu.add.button("Back", partial(to_controls,
                                    menu=menu,
                                    surface=surface,
                                    main=main))
    menu.mainloop(surface=surface)


if __name__ == '__main__':
    main_menu()
