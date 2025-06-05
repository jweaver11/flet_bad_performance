'''
The main 'story' page. The default page that all others work through.
Each section of this main page contains another 'page',
so they can update themselves dynamically
'''
import flet as ft
from workspaces.story import story
from hud.menu_bar import create_menu_bar
from hud.rails import create_rails


# Container for 1 or more pagelets open on main right side of screen (work area)
pagelets_container = ft.Container(
    expand=True,
    padding=4,
    border_radius=ft.border_radius.all(20),  # 20px radius on all corners
    bgcolor=ft.Colors.GREY_900,
    content=ft.Row(
        controls=[
            ft.Column(controls=[ft.Text("Pagelets container")])
        ]
    )
)


# MAIN FUNCTION TO RUN PROGRAM ---------------------------------------------------------
def main(page: ft.Page):

    # Adds our page title and theme
    title = "StoryBoard -- " + story.title + " -- Saved status"
    page.title = title
    #page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    # Create our menu bar for the top of the page
    menubar = create_menu_bar(page)

    all_workspaces_rail, active_rail = create_rails(page) 
    #pagelets = pagelet page


    # RENDER OUR PAGE
    # Add our top menubar to the page
    page.add(menubar)

    # Add the rest of the page
    page.add(ft.Row(
        spacing=0,  # No space between elements
        expand=True,  # Makes sure it takes up the entire window/screen

        controls=[
            all_workspaces_rail,  # Main rail of all available workspaces
            ft.VerticalDivider(width=0, thickness=2),

            active_rail,    # Rail for the selected workspace
            ft.VerticalDivider(thickness=2),   # Divider between rail and work area
            
            pagelets_container,    # Work area for pagelets
        ],
    ),

)



ft.app(main)