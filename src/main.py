# The main 'story' page. The default page that all others work through
import flet as ft


from handlers.story import story
from hud.menu_bar import create_menu_bar
from handlers.rail_handler import active_workspace_rail
from hud.workspaces_rail import all_workspaces_rail_container


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
active_workspace_container = ft.Container(
    border = ft.border.all(0, ft.Colors.GREEN_200),
    expand=True,
    content=ft.Row(
        spacing=0,
        controls=[
            ft.Container(padding=ft.padding.all(15), content=
                #active_workspace_rail_container,
                ft.Column(  # Adds rail fot he active workspace
                    # horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
                    # scroll=ft.ScrollMode.AUTO,
                    controls=active_workspace_rail  # Adds whatever rail is active as a list of items
                ), 
            ),
            ft.VerticalDivider(width=1, thickness=1),   # Divider between rail and work area
            ft.Column(controls=[pagelets_container], expand=True)   # Adds container for work area
        ]
    )
    # [] of active pagelets, save to user so they wont vanish when app closed
)
                
# timer = time.Timer()

# MAIN FUNCTION TO RUN PROGRAM ---------------------------------------------------------
def main(page: ft.Page):

    title = "StoryBoard -- " + story.title + " -- Saved status"
    page.title = title  # Set title
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)    # Set theme

    # Create our menu bar for the top of the page
    menubar = create_menu_bar(page)

    page.add(ft.Row([menubar]))
    page.add(ft.Row(
                spacing=0, 
                expand=True,  

                controls=[
                    all_workspaces_rail_container,  # Sub-Rail for active workspace
                    active_workspace_container,    # Work area for pagelets
                ],
            ),)



ft.app(main)