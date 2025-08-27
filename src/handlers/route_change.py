import flet as ft
from models.story import Story

# Called whenever a new story is laoded
def route_change(page: ft.Page, new_story: Story=None) -> Story:

    page.views.clear()
    page.controls.clear()
    
    if new_story is not None:
        
        #new_story.startup(page)  # Call startup to load story data and UI elements

        page.views.append(new_story)

        page.route = new_story.route

        page.update()

        print("Route change:", page.route)

    else:
        view = ft.View(
            "/",
            [
                ft.Text("No active story. Please create or load a story from the menu."),
            ],
        )
        page.views.append(view)
        page.update()

    #return new_story