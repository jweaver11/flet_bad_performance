''' Main productivity windows beneath the menu bar
and to the right of the navigation rail '''

import flet as ft
from hud.menu_bar import create_menu_bar
from hud.workspaces_rail import workspaces_rail_container
from handlers.rail_handler import workspace_rail


# Container for 1 or more pagelets open on main right side of screen (work area)
pagelets_container = ft.Container(
    border = ft.border.all(0, ft.Colors.BLUE_200),
    expand=True,
    padding=4,
    margin=10,
    content=ft.Row(
        controls=[
            ft.Column(controls=[ft.Text("Pagelets container")])
        ]
    )
)

# Parent container for entire page minus the menubar and workspaces rail
workspace_container = ft.Container(
    border = ft.border.all(0, ft.Colors.GREEN_200),
    expand=True,
    width=160,
    content=ft.Row(
        spacing=0,
        controls=[
            ft.Column(controls=workspace_rail),  # Adds the rail for whichever workspace selected
            ft.VerticalDivider(width=0, thickness=2),   # Divider between rail and work area
            ft.Column(controls=[pagelets_container], expand=True)   # Adds container for work area
        ]
    )
    # [] of active pagelets, save to user so they wont vanish
)


# Render page that is main working page of the app
def work_page(page: ft.Page):

    # Create our menu bar for the top of the page
    menubar = create_menu_bar(page)

    # Renders our work page
    return ft.View(
        "/work",
        controls=[
            ft.Row([menubar]),  # Add menu bar at top of page

            # Add everything else to the page, from left to right
            ft.Row(
                spacing=0, 
                expand=True,  

                controls=[
                    workspaces_rail_container,  # Sub-Rail for active workspace
                    workspace_container,    # Work area for pagelets
                ],
            ),
        ],
)


