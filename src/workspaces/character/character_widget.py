import flet as ft
from handlers.create_widgets import new_widget


# Function to create our list of controls for the widget formatting
# Under the story object
def create_character_widget(name):

    # list of flet controls, nested within a column
    list = [
        ft.Text("title 1")
    ]


    # return finished widget
    return new_widget(name, list)