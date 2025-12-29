'''
The main file to run the application.
Initializes the app, settings, page data, and renders our UI onto the page
'''

import flet as ft
from models.app import app
from handlers.route_change import route_change
import asyncio



# Main function
def main(page: ft.Page):

    page.views.append(ft.View([ft.Text("Loading view here", expand=True)], "/loading"))
    page.update()

    # Set our route change function to be called on route changes
    page.on_route_change = route_change 
    
    # Load settings and previous story (if one exists)
    app.load_settings(page)             
    asyncio.create_task(app.load_previous_story(page))    # If a previous story was loaded, we load its route/view here


    


# Runs the app
if __name__ == "__main__":
    ft.run(main)
