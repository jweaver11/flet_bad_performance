'''
The main file to run the application.
Initializes the app, settings, page data, and renders our UI onto the page
'''

import flet as ft
from models.app import app
from handlers.route_change import route_change
from constants.init import init_settings, init_load_saved_stories
from ui.active_rail import Active_Rail
from ui.menu_bar import create_menu_bar
from ui.workspace import create_workspace
from ui.workspaces_rail import Workspaces_Rail



# Main function
def main(page: ft.Page):

    # Set initial route and our route change function to be called on route changes
    page.route = "/"    # This is changed by any the active story if there is one inside of init_load_saved_stories
    page.on_route_change = route_change 

    
    # Initializes our settings, stories
    init_settings(page)
    init_load_saved_stories(page)   # Changes route to active story if there is one

    # Sets our theme modes and color schemes based on app settings (first start is dark and blue)
    page.theme = ft.Theme(color_scheme_seed=app.settings.data.get('theme_color_scheme', "blue"))
    page.dark_theme = ft.Theme(color_scheme_seed=app.settings.data.get('theme_color_scheme', "blue"))
    page.theme_mode = app.settings.data.get('theme_mode', 'dark')
   
    # Sets the title of our app, padding, and maximizes the window
    page.padding = ft.padding.only(top=0, left=0, right=0, bottom=0)    # non-desktop should have padding
    page.window.maximized = app.settings.data.get('window_maximized', True)


    # Called to create the page view if no stories exist
    def create_page_if_no_stories_exist() -> ft.Control:
        ''' Gives us the menubar, initial rail, and large buttons to create your first story'''

        page.title = "StoryBoard"
        page.padding = ft.padding.only(top=0, left=0, right=0, bottom=0)    # non-desktop should have padding
        
        menubar = create_menu_bar(page)   


        # Create our rails inside of app so we can access it as an object and store preferences
        all_workspaces_rail = Workspaces_Rail(page)  # Create our all workspaces rail
        active_rail = ft.Container(
            alignment=ft.alignment.top_center,  
            padding=ft.padding.only(top=10, bottom=10, left=4, right=4),
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),
            width=app.settings.data['active_rail_width'],  
            content=ft.Text("Create a story to get started!")
        )

        # Create our workspace container to hold our widgets
        workspace = create_workspace(page)  # render our workspace containing our widgets 
        #workspace.alignment = ft.MainAxisAlignment.CENTER

        # Save our 2 rails, divers, and our workspace container in a row
        row = ft.Row(
            spacing=0,  # No space between elements
            expand=True,  # Makes sure it takes up the entire window/screen

            controls=[
                all_workspaces_rail,  # Main rail of all available workspaces
                ft.VerticalDivider(width=2, thickness=2, color=ft.Colors.OUTLINE_VARIANT),   # Divider between workspaces rail and active_rail

                active_rail,    # Rail for the selected workspace
                active_rail_divider,   # Divider between rail and work area
                
                workspace,    # Work area for pagelets
            ],
        )

        # Format our page. Add our menubar at the top, then then our row built above
        view = ft.View(
            spacing=0, 
            padding=ft.padding.only(top=0, left=0, right=0, bottom=0),
            controls=[
                menubar, 
                row,
            ]
        )
        
        return view

    # Called if there is no active story, but stories do exist
    def create_page_if_no_stories_active() -> ft.Control:
        ''' Creates our page view with a menubar, all_workspaces_rail, and two large buttons for create and open story'''

        page.title = "StoryBoard"
        page.padding = ft.padding.only(top=0, left=0, right=0, bottom=0)    # non-desktop should have padding
        
        menubar = create_menu_bar(page)   

        # Create our rails inside of app so we can access it as an object and store preferences
        all_workspaces_rail = Workspaces_Rail(page)  # Create our all workspaces rail
        active_rail = Active_Rail(page)  # Container stored in story for the active rails

        # Create our workspace container to hold our widgets
        workspace = create_workspace(page)  # render our workspace containing our widgets 

        # Save our 2 rails, divers, and our workspace container in a row
        row = ft.Row(
            spacing=0,  # No space between elements
            expand=True,  # Makes sure it takes up the entire window/screen

            controls=[
                all_workspaces_rail,  # Main rail of all available workspaces
                ft.VerticalDivider(width=2, thickness=2, color=ft.Colors.OUTLINE_VARIANT),   # Divider between workspaces rail and active_rail

                active_rail,    # Rail for the selected workspace
                active_rail_divider,   # Divider between rail and work area
                
                workspace,    # Work area for pagelets
            ],
        )

        # Format our page. Add our menubar at the top, then then our row built above
        view = ft.View(
            spacing=0, 
            padding=ft.padding.only(top=0, left=0, right=0, bottom=0),
            controls=[
                menubar, 
                row,
            ]
        )
        
        return view



    # The divider to the right of the active rail
    active_rail_divider = ft.Container(
        width=10,   # Total width of the GD, so its easier to find with mouse
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),  # Matches our bg color to the active_rail
        # Thin vertical divider, which is what the app will actually drag
        content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.OUTLINE_VARIANT),
        padding=ft.padding.only(left=8),  # Push the 2px divider ^ to the right side
    )
       

    # If we loaded our stories, and there is no active story, we load 1 of 2 views
    if page.route == "/":

        page.views.clear()

        # If no stories exist, load this view
        if len(app.stories) == 0:
            page.views.append((create_page_if_no_stories_exist()))
            print("No stories exist")
        # If stories exist, but no active story, load this view
        else:
            page.views.append((create_page_if_no_stories_active()))
            print("Stories exist, but no active story")
        
    page.update()


# Runs the app
ft.app(main)