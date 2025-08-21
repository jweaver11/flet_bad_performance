'''
The main 'story' page. The default page that all others work through.
Each section of this main page contains another 'page',
so they can update themselves dynamically
'''

import flet as ft
from models.user import user
from models.settings import Settings
from ui.menu_bar import create_menu_bar
from ui.workspaces_rails import All_Workspaces_Rail
from ui.active_rail import create_active_rail
from ui.workspace import create_workspace


# MAIN FUNCTION TO RUN PROGRAM ---------------------------------------------------------
def main(page: ft.Page):

    
    
    # Checks if our user settings exist. This will only run if the user is newly created
    # Otherwise, when the user loads in, their settings will load as well
    if user.settings is None:
        # We create our user settings here because we need the page reference
        user.settings = Settings(page)  

    user.active_story.startup(page)

   
    # Adds our page title and theme
    title = "StoryBoard -- " + user.active_story.title + " -- Saved status"

    # Sets our theme modes, but we start dark
    # If theme mode un-set, set dark...
    page.theme = ft.Theme(color_scheme_seed=user.settings.data['theme_color_scheme'])
    page.dark_theme = ft.Theme(color_scheme_seed=user.settings.data['theme_color_scheme'])
    page.theme_mode = user.settings.data['theme_mode']
   
    # Sets the title of our app, padding, and maximizes the window
    page.title = title
    page.padding = ft.padding.only(top=0, left=0, right=0, bottom=0)
    page.window.maximized = True


    # Create our page elements as their own pages so they can update
    menubar = create_menu_bar(page)   

    
    user.all_workspaces_rail = All_Workspaces_Rail(page)  # Create our all workspaces rail

    
    # Just create it each time
    user.active_rail = create_active_rail(page)  # Render whichever rail is active

    workspace = create_workspace(page)# render our workspace containing our widgets

    def show_horizontal_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    # Left pin reisizer method and variable
    def move_active_rail_divider(e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and user.active_rail.width < page.width/2) or (e.delta_x < 0 and user.active_rail.width > 100):
            user.active_rail.width += e.delta_x
            print("Active rail width: " + str(user.active_rail.width))
        user.active_rail.update()
        user.active_story.widgets.update()
        user.active_story.master_stack.update()
    active_rail_resizer = ft.GestureDetector(
        content=ft.Container(
            width=10,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),
            padding=ft.padding.only(left=8),  # Push the 2px divider to the right side
            content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.OUTLINE_VARIANT)
        ),
        on_pan_update=move_active_rail_divider,
        on_hover=show_horizontal_cursor,
    )

    # Save our 2 rails, dividers, and our workspace container in a row
    row = ft.Row(
        spacing=0,  # No space between elements
        expand=True,  # Makes sure it takes up the entire window/screen

        controls=[
            user.all_workspaces_rail,  # Main rail of all available workspaces
            ft.VerticalDivider(width=2, thickness=2, color=ft.Colors.OUTLINE_VARIANT),   # Divider between workspaces rail and active_rail

            user.active_rail,    # Rail for the selected workspace
            active_rail_resizer,   # Divider between rail and work area
            
            workspace,    # Work area for pagelets
        ],
    )
    

    # Format our page. Add our menubar at the top, then then our row built above
    col = ft.Column(
        spacing=0, 
        expand=True, 
        controls=[
            menubar, 
            row,
        ]
    )

    page.add(col)


ft.app(main)


# Add custom title bar