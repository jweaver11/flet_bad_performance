''' Main productivity windows beneath the menu bar
and to the right of the navigation rail '''

import flet as ft
from hud.menu_bar import create_menu_bar
from hud.workspaces_rail import workspaces_rail_container
from workspace_rails.character_rail import characters_rail


# Container for 1 or more pagelets open on main right side of screen
pagelets_container = ft.Container(
    border = ft.border.all(0, ft.Colors.BLUE_200),
    # Add more widgets here as needed
    expand=True,
    content=ft.Row(
        controls=[
            ft.Column(controls=[ft.Text("Pagelets container")])
        ]
    )
)

# Using pagelets somehow someway somehwere
# Add workspace containers for pop out options
workspace_container = ft.Container(
    border = ft.border.all(0, ft.Colors.GREEN_200),
    # Add more widgets here as needed
    expand=True,
    width=160,
    content=ft.Row(
        spacing=0,
        controls=[
            ft.Column(controls=[characters_rail]),
            ft.VerticalDivider(width=1, thickness=2),
            ft.Column(controls=[pagelets_container], expand=True)
        ]
    )
)


# Render page that is main working page of the app
def work_page(page: ft.Page):

    # Create our menu bar for the top of the page
    menubar = create_menu_bar(page)

    # Renders our work page
    return ft.View(
        "/work",
        controls=[
            # Add the menu bar to the top
            ft.Row([menubar]),

            # Add everything else to the page, from left to right
            ft.Row(
                spacing=0,  # No spacing between containers
                expand=True,    # Cover the rest of the page
                # The rest of the controls (widgets) to the page
                controls=[
                    workspaces_rail_container,
                    workspace_container,
                ],
            ),
        ],
)


