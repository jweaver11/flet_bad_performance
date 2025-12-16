'''
The main file to run the application.
Initializes the app, settings, page data, and renders our UI onto the page
'''

import flet as ft
from models.app import app
from handlers.route_change import route_change
from models.views.home import create_home_view



# Main function
def main(page: ft.Page):

    # Home view (No stories/main page), story view, settings view 


    # Set our route change function to be called on route changes
    page.on_route_change = route_change 

    # Load settings and previous story (if one exists)
    app.load_settings(page)             
    app.load_previous_story(page)       # If a previous story was loaded, it will load here

    # If route is default (No story was loaded), create a view for that
    if page.route == "/":
        
        page.views.append(create_home_view(page))
        page.update()
    


# Runs the app
ft.app(main)