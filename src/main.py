'''
The main file to run the application.
Initializes the app, settings, page data, and renders our UI onto the page
'''

import flet as ft
from models.app import app
from handlers.route_change import route_change
from models.views.loading import create_loading_view
import asyncio

ft.context.disable_auto_update()

# Main function
def main(page: ft.Page):

    # Set loading view here if we want to use one
    # Our loading view while we setup the app
    page.views.append(create_loading_view(page))
    page.update()

    # Set our route change function to be called on route changes
    page.on_route_change = route_change 
    
    # Load settings and previous story (if one exists)
    app.load_settings(page)             

    # Load our previous story if one was active. If not, it will give us our home view
    asyncio.create_task(app.load_previous_story(page)) 


# Runs the app
if __name__ == "__main__":
    ft.run(main)
