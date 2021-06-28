import pygame_menu
from functools import partial
from pygame_menu.examples import create_example_window

from Smooth.game_functions_smooth import change_snake_color, change_apple_color, \
    change_speed, change_screen_color, change_screen_height, change_screen_width, change_bad_apple_color

from Smooth.Objects_smooth import Snake, Screen, Apple, Bad_Apple, Wall


def main_menu():
    surface = create_example_window("Menu", (Screen.height, Screen.width))

    menu = pygame_menu.Menu(
        height=400,
        width=400,
        title="Main menu"
    )

    menu.add.button("Play", play)
    menu.add.button("Settings", partial(to_settings, menu=menu, surface=surface, main=True))

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
    menu.add.button("Color", partial(to_color_settings, menu, surface, main))
    menu.add.button("Controls", partial(to_controls, menu, surface, main))
    if main:
        menu.add.button("Back", partial(from_settings_to_main_menu, menu))
    else:
        menu.add.button("Back", partial(from_settings_to_pause_menu, menu))

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
    from Smooth.smooth_snake import game

    game()


def create_pause_menu(on):
    menu = pygame_menu.Menu(
        height=200,
        width=200,
        title="Paused"
    )
    if on:
        surface = create_example_window("Menu", (Screen.height, Screen.width))

        menu.add.button("Continue", menu.disable)
        menu.add.button("Settings", partial(to_settings, menu, surface, False))
        menu.add.button("Quit", main_menu)

        menu.mainloop(surface)
    return menu


def color(surface, main):
    # print("Color", main)
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
        ("White", "white"),
        ("Pink", "pink"),
        ("Black", "black"),
        ("Purple", "purple")
    ]
    menu.add.selector("Snake color: ",
                      default=list_of_colors.index((Snake.color.title(), Snake.color)),
                      items=list_of_colors,
                      onchange=change_snake_color)
    menu.add.selector("Apple color: ",
                      default=list_of_colors.index((Apple.color.title(), Apple.color)),
                      items=list_of_colors,
                      onchange=change_apple_color)
    menu.add.selector("Bad apple color: ",
                      default=list_of_colors.index((Bad_Apple.color.title(), Bad_Apple.color)),
                      items=list_of_colors,
                      onchange=change_bad_apple_color)
    menu.add.selector("Background color",
                      default=list_of_colors.index((Screen.color.title(), Screen.color)),
                      items=list_of_colors,
                      onchange=change_screen_color)

    menu.add.button("Back", partial(back_from_colors_to_settings, menu, surface, main))

    menu.mainloop(surface)


def controls(surface, main):
    menu = pygame_menu.Menu(
        height=400,
        width=400,
        title="Controls",
    )

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

    label = menu.add.label("Please, input number")
    label_done = menu.add.label("Done!")
    label.hide()
    label_done.hide()

    def commit():
        for index in range(len(list_of_buttons)):
            get_value(list_of_buttons[index], list_of_functions[index])

    menu.add.button("Commit", commit)

    menu.add.button("Back", partial(to_settings, menu=menu, surface=surface, main=main))

    menu.mainloop(surface)


if __name__ == '__main__':
    main_menu()
