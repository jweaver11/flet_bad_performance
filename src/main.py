'''
The main 'story' page. The default page that all others work through.
Each section of this main page contains another 'page',
so they can update themselves dynamically
'''

import flet as ft
from models.user import user
from ui.menu_bar import create_menu_bar
from ui.workspaces_rail import create_rails
from ui.active_rail import create_active_rail
from ui.workspace import create_workspace


# MAIN FUNCTION TO RUN PROGRAM ---------------------------------------------------------
def main(page: ft.Page):

    story = user.active_story  # Get our story object from the user


    # Adds our page title and theme
    title = "StoryBoard -- " + story.title + " -- Saved status"
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.title = title
    page.padding=ft.padding.only(top=0, left=0, right=0, bottom=0)
    page.window.maximized = True

    # Create our page elements as their own pages so they can update
    menubar = create_menu_bar(page)     # menubar
    all_workspaces_rail = create_rails(page)   # all workspaces rail and active rail
    active_rail = create_active_rail(page)  # Render whichever rail is active
    workspace = create_workspace(page, story)  # render our workspace containing our widgets

    # Save our 2 rails, dividers, and our workspace container in a row
    row = ft.Row(
        spacing=0,  # No space between elements
        expand=True,  # Makes sure it takes up the entire window/screen

        controls=[
            all_workspaces_rail,  # Main rail of all available workspaces
            ft.VerticalDivider(width=2, thickness=2, trailing_indent=10, leading_indent=10),

            active_rail,    # Rail for the selected workspace
            ft.VerticalDivider(width=2, thickness=2, trailing_indent=10, leading_indent=10),   # Divider between rail and work area
            
            workspace,    # Work area for pagelets
        ],
    )

    # Format our page. Add our menubar at the top, then then our row built above
    col = ft.Column(
        spacing=0, 
        expand=True, 
        controls=[
            menubar, 
            ft.Divider(color=ft.Colors.PRIMARY, height=2, thickness=2, opacity=0.2),
            row
        ]
    )

    page.add(col)


ft.app(main)


# Add custom title bar 