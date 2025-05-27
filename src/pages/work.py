''' Main productivity windows beneath the menu bar
and to the right of the navigation rail '''

import flet as ft
from hud.menu_bar import create_menu_bar
from hud.nav_rail import rail
from hud.workspace_rail import workspace_rail
from models.characters import characters
from models.characters import Character

# Using pagelets somehow someway somehwere
workspaces = ft.Column(
    [
        ft.Text("Body!"),
        ft.Text("I wanne be to the right of the navbar"),
        # Add more widgets here as needed
    ],
    alignment=ft.MainAxisAlignment.START,
    expand=True,
)

# Render page that is main working page of the app
def work_page(page: ft.Page):

    # Set and add the menu bar at top of the page
    menubar = create_menu_bar(page)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    Character_one = Character("Johnny")
    characters.append(Character("Karate"))  # Create object and write to list in one line
    characters.append(Character_one)

    for character in characters:
        print(character.name)

    # Renders our work page
    return ft.View(
        "/work",
        [
            ft.Row([menubar]),
            ft.Row(
                [
                    rail,   # Add navigation rail to page
                    ft.VerticalDivider(width=10),
                    workspace_rail,
                    workspaces,
                ],
                expand=True
            )
        ]
)


