''' Main productivity windows beneath the menu bar
and to the right of the navigation rail '''

import flet as ft
from hud.menu_bar import create_menu_bar
from hud.navigation_rail import navigation_rail
from widgets.widget_rails.character_rail import character_rail


navigation_rail_container = ft.Container(
    border = ft.border.all(0, ft.Colors.GREY_200),
    alignment=ft.alignment.center,  # Aligns content to the 
    width=160,
    content=ft.Row(
        controls=[
            navigation_rail,
            ft.VerticalDivider(width=0, thickness=2),
        ]
    ),
)

# Using pagelets somehow someway somehwere
# Add workspace containers for pop out options
workspaces = ft.Container(
    border = ft.border.all(0, ft.Colors.BLUE),
    # Add more widgets here as needed
    expand=True,
    content=ft.Row(
        controls=[
            ft.Column(width=160, controls=[character_rail]),
            ft.VerticalDivider(width=1, thickness=2),
            ft.Column(controls=[ft.Text("workspaces container")])
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

        [
            # Add the menu bar to the top
            ft.Row([menubar]),

            # Add everything else to the page, from left to right
            # The controls this adds should be dynamic and switch from page to page
            ft.Row(
                spacing=0,  # No spacing between containers
                expand=True,    # Cover the rest of the page
                # The rest of the controls (widgets) to the page
                controls=[
                    navigation_rail_container,

                    workspaces,
                ],
            ),

            #nav_rail_container,

           # work_rail_container
        ],
)


