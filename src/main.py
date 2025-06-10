'''
The main 'story' page. The default page that all others work through.
Each section of this main page contains another 'page',
so they can update themselves dynamically
'''
import flet as ft
from workspaces.story import story
from hud.menu_bar import create_menu_bar
from hud.rails import create_rails
from hud.widgets import create_widgets


# MAIN FUNCTION TO RUN PROGRAM ---------------------------------------------------------
def main(page: ft.Page):

    # Adds our page title and theme
    title = "StoryBoard -- " + story.title + " -- Saved status"
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.window.title_bar_hidden = True

    # Function to maximize/restore window
    def maximize_restore(e):
        page.window.maximized = not page.window.maximized
        page.update()

    # Function to minimize window
    def minimize(e):
        page.window.minimized = True
        page.update()

    title_bar = ft.Row(
        spacing=0,
        controls=[
            ft.WindowDragArea(
                expand=True,
                content=ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Text(title),
                ),
            ),
            ft.IconButton(ft.Icons.MINIMIZE, on_click=minimize),
            ft.IconButton(ft.Icons.SQUARE_OUTLINED, on_click=maximize_restore),
            ft.IconButton(ft.Icons.CLOSE, on_click=lambda _: page.window.close()),
        ]
    )

    # Create our page elements as their own pages so they can update
    menubar = create_menu_bar(page)     # menubar
    all_workspaces_rail, active_rail = create_rails(page)   # all workspaces rail and active rail
    widgets = create_widgets(page)        # pagelets 

    page.padding=ft.padding.only(top=0, left=0, right=0, bottom=0)

    # RENDER OUR PAGE
    # Custom title_bar so colors batch better
    page.add(title_bar)
    # Add our top menubar to the page
    page.add(menubar)

    # Add the rest of the page
    page.add(ft.Row(
        spacing=0,  # No space between elements
        expand=True,  # Makes sure it takes up the entire window/screen

        controls=[
            all_workspaces_rail,  # Main rail of all available workspaces
            ft.VerticalDivider(width=2, thickness=2),

            active_rail,    # Rail for the selected workspace
            ft.VerticalDivider(width=2, thickness=2),   # Divider between rail and work area
            ft.Column(width=10),
            
            widgets,    # Work area for pagelets
        ],
    ),

)


ft.app(main)