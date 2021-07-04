import pygame_menu
from functools import partial
from pygame_menu.examples import create_example_window

from game_functions_smooth import \
    change_speed, change_screen_height, change_screen_width, \
    change_mode, change_color, change_net_host, change_net_port
from Objects_smooth import Snake, Screen, Apple, Bad_Apple, Mode, Wall, Second_Snake


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


def to_settings(menu, surface, main):
    menu.close()
    menu.disable()

    settings(surface, main)


def to_color_settings(menu, surface, main):
    menu.close()
    menu.disable()

    color(surface, main)


def settings(surface, main):
    # print(main)
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
    if Mode.player == "online":
        network_settings.show()

    if main:
        menu.add.button("Back", partial(from_settings_to_main_menu,
                                        menu=menu))
    else:
        menu.add.button("Back", partial(from_settings_to_pause_menu,
                                        menu=menu,
                                        surface=surface,
                                        main=main))

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

    host = menu.add.text_input("Host: ")
    port = menu.add.text_input("Port: ")

    def commit():
        host_get = host.get_value()
        port_get = port.get_value()
        change_net_host(host_get)
        change_net_port(port_get)

    menu.add.button("Commit", commit)

    menu.add.button("Back", partial(back_from_colors_to_settings,
                                    menu=menu,
                                    surface=surface,
                                    main=main))
    menu.mainloop(surface)


def from_settings_to_main_menu(menu):
    menu.close()
    menu.disable()

    main_menu()


def from_settings_to_pause_menu(menu: pygame_menu.Menu):
    menu.close()
    menu.disable()

    create_pause_menu(True)


def back_from_colors_to_settings(menu, surface, main):
    menu.close()
    menu.disable()

    settings(surface, main)


def to_controls(menu, surface, main):
    # print(main)
    menu.close()
    menu.disable()

    controls(surface, main)


def play():
    from smooth_snake import single_game
    from smooth_snake import two_players, online_two_players

    if Mode.player == "Two":
        two_players()
    elif Mode.player == "One":
        single_game()
    elif Mode.player == "Online":
        online_two_players()


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


def to_help_menu(menu, surface, main):
    menu.close()
    menu.disable()

    help_menu(surface, main)


def help_menu(surface, main):
    height = 400
    width = 400
    menu = pygame_menu.Menu(
        height=height,
        width=width,
        title="Help"
    )

    menu.add.button('Back', partial(from_settings_to_pause_menu, menu=menu))

    menu.mainloop(surface)


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
    menu.add.selector(title="Snake color: ",
                      default=list_of_colors.index((Snake.color.title(), Snake.color)),
                      items=list_of_colors,
                      onchange=partial(change_color, Snake))

    menu.add.selector(title="Apple color: ",
                      default=list_of_colors.index((Apple.color.title(), Apple.color)),
                      items=list_of_colors,
                      onchange=partial(change_color, Apple))

    menu.add.selector(title="Bad apple color: ",
                      default=list_of_colors.index((Bad_Apple.color.title(), Bad_Apple.color)),
                      items=list_of_colors,
                      onchange=partial(change_color, Bad_Apple))
    if Mode.player == "Two":
        menu.add.selector(title="Second snake color: ",
                          default=list_of_colors.index((Second_Snake.color.title(), Second_Snake.color)),
                          items=list_of_colors,
                          onchange=partial(change_color, Second_Snake))

    menu.add.selector(title="Wall color",
                      default=list_of_colors.index((Wall.color.title(), Wall.color)),
                      items=list_of_colors,
                      onchange=partial(change_color, Wall))

    menu.add.selector(title="Background color",
                      default=list_of_colors.index((Screen.color.title(), Screen.color)),
                      items=list_of_colors,
                      onchange=partial(change_color, Screen))

    menu.add.button("Back", partial(back_from_colors_to_settings,
                                    menu=menu,
                                    surface=surface,
                                    main=main))

    menu.mainloop(surface)


def controls(surface, main):
    menu = pygame_menu.Menu(
        height=400,
        width=400,
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
        ("Width: ", Screen.width)
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

    menu.add.button("Back", partial(to_settings,
                                    menu=menu,
                                    surface=surface,
                                    main=main))

    menu.mainloop(surface)


if __name__ == '__main__':
    main_menu()
