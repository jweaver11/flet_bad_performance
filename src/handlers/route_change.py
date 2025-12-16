import flet as ft
from models.views.story import Story

# Called whenever a new story is laoded
def route_change(e: ft.RouteChangeEvent) -> Story:
    ''' Handles changing our page view based on the new route '''
    from models.app import app
    from models.views.home import create_home_view
    from styles.snack_bar import Snack_Bar

    # Grabs our page from the event for easier reference
    page: ft.Page = e.page

    # Clear our views and any existing controls
    page.views.clear()
    page.controls.clear()

    # If our route is the home page, we just need to load the home view and return
    if page.route == "/":
        page.views.append(create_home_view(page))
        page.update()
        return
    
    # Else if its our settings page, we load that view and return
    elif page.route == "/settings":
        page.views.append(app.settings)
        page.update()
        return

    # Otherwise its a story route, so we need to find which one it is
    else:

        new_story = None    # Set new story to none intially to handle routes that don't match any stories

        # Run through our stories and see which ones route matches our new route
        for story in app.stories.values():
            # If it matches, set our new story 
            if story.route == page.route:
                new_story = story
                app.settings.data['active_story'] = story.title
                app.settings.save_dict()
                break
            
        
        # If we have a story route that matches our new route, load it to the page views
        if new_story is not None:
            
            # Load our new stories data and builds its UI, then adds it to the page
            new_story.startup()
            page.views.append(new_story)

        # Otherwise, give us a blank page
        else:
            print("Error loading story for route: " + page.route)
            page.open(
                Snack_Bar(
                    content=ft.Text(
                        f"Error loading story for route: {page.route}",
                        weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, expand=True
                        )
                    )
                )
        
        page.update()