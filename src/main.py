# The main 'story' page. The default page that all others work through
import flet as ft

from pages.work import work_page
from pages.welcome import welcome_page
from pages.settings import settings_page
                

# MAIN FUNCTION TO RUN PROGRAM ---------------------------------------------------------
def main(page: ft.Page):

    page.title = "Project - Name"

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(work_page(page))
        elif page.route == "/welcome":
            page.views.append(welcome_page(page))
        elif page.route == "/settings":
            page.views.append(settings_page(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        page.go(page.views[-1].route)

    def view_pop(view):
        page.views.pop()  # Remove the current view (page)
        top_view = page.views[-1]
        page.go(top_view.route)  # Go back to the previous route

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main)