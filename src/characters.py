import flet as ft

# Class for each character. Requires passing in a name
class Character:
    def __init__(self, name):
        self.name = name
        
    age = 0


def characters_view(page):
    return ft.View(
        "/",
        [ft.Text("This is Page One"), ft.ElevatedButton("Go to Page Two", on_click=lambda _: page.go("/two"))]
    )
