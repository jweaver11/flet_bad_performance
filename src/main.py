# The main 'story' page. The default page that all others work through
import flet as ft
from handlers.story import story
from hud.menu_bar import create_menu_bar
from handlers.rail_handler import active_workspace_rail
from hud.workspaces_rail import all_workspaces_rail

# Container for all available workspaces. On left most side of page
all_workspaces_rail_container = ft.Container(
    border = ft.border.all(0, ft.Colors.RED_200),
    alignment=ft.alignment.center,  # Aligns content to the 
    width=160,
    content=ft.Row(
        controls=[
            all_workspaces_rail,
        ]
    ),
)


# Container for the select/active workspace rail.
active_workspace_rail_container = ft.Container(
    border = ft.border.all(0, ft.Colors.YELLOW),
    #expand=True,
    width=250,
    padding=ft.padding.all(15),
    content=ft.Column(  # Adds rail fot he active workspace
        # horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
        # scroll=ft.ScrollMode.AUTO,
        controls=active_workspace_rail  # Adds whatever rail is active as a list of items
    ),           
)


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


# MAIN FUNCTION TO RUN PROGRAM ---------------------------------------------------------
def main(page: ft.Page):

    # Adds our page title and theme
    title = "StoryBoard -- " + story.title + " -- Saved status"
    page.title = title
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    # Create our menu bar for the top of the page
    menubar = create_menu_bar(page)
    # Create our container for the menu bar
    menu_bar_container = ft.Container(
        bgcolor=ft.Colors.GREY_900,     # Set background color
        border_radius=ft.border_radius.all(20),  # 20px radius on all corners

        content=ft.Row(
            spacing=None,
            controls=[
                menubar,    # Menubar on left
                ft.Container(expand=True),  # empty space in middle of menubar
                ft.TextButton("Feedback"),  # Feedback button
                ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icon(ft.Icons.SETTINGS)),   # Settings button
                ft.TextButton("Account Name"),  # users account name
                ft.CircleAvatar(scale=.8),  # users avatar
            ]
        )
    )


    # RENDER OUR PAGE
    # Add our top menubar to the page
    page.add(menu_bar_container)

    # Add the rest of the page
    page.add(ft.Row(
        spacing=0,  # No space between elements
        expand=True,  # Makes sure it takes up the entire window/screen

        controls=[
            all_workspaces_rail_container,  # Main rail of all available workspaces
            ft.VerticalDivider(width=0, thickness=2),

            active_workspace_rail_container,    # Rail for the selected workspace
            ft.VerticalDivider(width=1, thickness=10),   # Divider between rail and work area
            
            pagelets_container,    # Work area for pagelets
        ],
    ),

)



ft.app(main)