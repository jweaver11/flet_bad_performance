'''
The main file to run the application.
Initializes the app, settings, page data, and renders our UI onto the page
'''

import flet as ft
from models.app import app
from handlers.route_change import route_change
from constants.init import init_settings, init_load_saved_stories
from ui.menu_bar import create_menu_bar
from ui.workspace import create_workspace



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

    # Set the window size as maximized or not
    if app.settings.data.get('page_is_maximized', True):
        page.window.maximized = app.settings.data.get('page_is_maximized', True)
    else:
        page.window.width = app.settings.data.get('page_width')
        page.window.height = app.settings.data.get('page_height')

    # Set our logic when page window is resized
    page.on_resized = lambda e: app.settings.page_resized(e)


    # Called to create the page view if no stories exist
    def create_page_if_no_stories_exist() -> ft.Control:
        ''' Gives us the menubar, initial rail, and large buttons to create your first story'''

        page.title = "StoryBoard"
        page.padding = ft.padding.only(top=0, left=0, right=0, bottom=0)    # non-desktop should have padding
        
        menubar = create_menu_bar(page)   

        # Create our workspace container to hold our widgets
        workspace = create_workspace(page)  # render our workspace containing our widgets 
        #workspace.alignment = ft.MainAxisAlignment.CENTER

        # Save our 2 rails, divers, and our workspace container in a row
        row = ft.Row(
            spacing=0,  # No space between elements
            expand=True,  # Makes sure it takes up the entire window/screen

            controls=[
                
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

        # Create our workspace container to hold our widgets
        workspace = create_workspace(page)  # render our workspace containing our widgets 

        # Save our 2 rails, divers, and our workspace container in a row
        row = ft.Row(
            spacing=0,  # No space between elements
            expand=True,  # Makes sure it takes up the entire window/screen

            controls=[
                
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