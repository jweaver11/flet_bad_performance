''' Main productivity windows beneath the menu bar
and to the right of the navigation rail '''

import flet as ft
from hud.menu_bar import create_menu_bar
from hud.nav_rail import rail

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
    # page.add(ft.Row([menubar]))

    # Renders our work page
    return ft.View(
        "/work",
        [
            ft.Row([menubar]),
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=10),
                    workspaces,
                ],
                expand=True
            )
        ]
)


