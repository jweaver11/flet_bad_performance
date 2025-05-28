''' Main productivity windows beneath the menu bar
and to the right of the navigation rail '''

import flet as ft
from hud.menu_bar import create_menu_bar
from hud.nav_rail import rail
from hud.rail_handler import workspace_rail
from models.characters import characters
from models.characters import Character
import models.characters

# Using pagelets somehow someway somehwere
# Add workspace containers for pop out options
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
                    ft.VerticalDivider(width=10),   # Divider between rails
                    workspace_rail, # Whichever workspace is selected from the navigation rail above
                    workspaces, # The workspaces to the right of the rail
                ],
                expand=True
            )
        ]
)


