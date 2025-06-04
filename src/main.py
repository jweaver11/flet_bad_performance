# The main 'story' page. The default page that all others work through
import flet as ft
from workspaces.story import story
from hud.menu_bar import create_menu_bar
from hud.workspaces_rail import active_workspace_rail
from hud.workspaces_rail import all_workspaces_rail

# Container for all available workspaces. On left most side of page
all_workspaces_rail_container = ft.Container(
    alignment=ft.alignment.center,  # Aligns content to the 
    content=ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
        alignment=ft.alignment.center,
        controls=[
            ft.Text(value=story.title, size=20),
            all_workspaces_rail,
            ft.TextButton(
                icon=ft.Icons.ADD_CIRCLE_ROUNDED, 
                text="Add Workspace", 
                on_click=lambda e: print("FAB clicked!"),
            ),
        ]
    ),
)


# Container for the select/active workspace rail.
active_workspace_rail_container = ft.Container(
    alignment=ft.alignment.center,  # Aligns content to the
    content=ft.Column(  # Adds rail fot he active workspace
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
        # scroll=ft.ScrollMode.AUTO,
        controls=active_workspace_rail,
    ),           
)


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
                ft.IconButton(ft.Icons.ACCOUNT_CIRCLE_OUTLINED),
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
            ft.VerticalDivider(thickness=2),   # Divider between rail and work area
            
            pagelets_container,    # Work area for pagelets
        ],
    ),

)



ft.app(main)