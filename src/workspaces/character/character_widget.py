import flet as ft
from handlers.create_widgets import new_widget

def ne_widget(title, body):
    cont = ft.Container(
        expand=True,
        padding=6,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_900,
        visible=True,
        content=ft.Column([
            ft.Row(     # Title of the widget
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[ft.TextButton(title)]
            ),
            ft.Container(       # Body of the widget
                expand=True,
                content=ft.Column(body) 
            )
    ]))
    # return our formatted container
    return cont

# Function to create our list of controls for the widget formatting
# Under the story object
def create_character_widget(name):

    # list of flet controls, nested within a column
    list = [
        ft.Text("title 1")
    ]

    print(name + " widget was created")

    # return finished widget
    return new_widget(name, list)