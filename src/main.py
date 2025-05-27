# The main 'story' page. The default page that all others work through
import flet as ft
from nav_rail import rail
from workspace import workspace
from menu_bar import create_menu_bar
                

# MAIN FUNCTION TO RENDER PAGE ---------------------------------------------------------
def main(page: ft.Page):

    

    # Set and add the menu bar at top of the page
    menubar = create_menu_bar(page)
    page.add(ft.Row([menubar]))

    # Adds our navbar and the workspace for the rest of the space
    page.add(
        ft.Row
        (
            [
                rail,   # Navigation rail on the left side of the page
                ft.VerticalDivider(width=10), # Divider between the nav rail and workspace
                workspace,  # Workspace for the main content of the page
                #footer
            ],
            expand=True
        )
    )


ft.app(main)