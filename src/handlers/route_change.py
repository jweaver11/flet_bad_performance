import flet as ft
from models.story import Story

# Called whenever a new story is laoded
def route_change(e: ft.RouteChangeEvent) -> Story:
    ''' Handles changing our page view based on the new route '''

    # Grabs our page from the event
    page = e.page

    # Clear our views and any existing controls
    page.views.clear()
    page.controls.clear()

    from models.app import app
    new_story = None    # Set new story to non intially to handle routes that don't match any stories

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
        page.views.append(new_story)
        # Set our new title to reflect this new loaded story
        page_title = "StoryBoard -- " + new_story.title + " -- Saved status"
        page.title = page_title

        print("Route change:", page.route)

    # Otherwise, give us a blank page
    else:
        from ui.menu_bar import create_menu_bar
        menu_bar = create_menu_bar(page)
        view = ft.View(
            "/",
            [
                menu_bar,
                ft.Text("No active story. Please create or load a story from the menu."),
            ],
        )

        # Add our default view and give it a page title
        page.views.append(view)
        page.title = "StoryBoard"
    
    page.update()

    #return new_story