import flet as ft

# Called whenever a new story is laoded
def route_change(page: ft.Page, new_story: ft.View) -> ft.View:
    print("Route change:", page.route)

    if page.route == new_story.route:
        return

    page.views.clear()  # Clear existing views 


    new_story.startup(page)  # Call startup to load story data and UI elements

    page.views.append(new_story)

    page.update()

    page.route = new_story.route

    page.update()

    #return new_story