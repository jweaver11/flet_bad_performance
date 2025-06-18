'''
Our 'widgets' page that returns the container for
all the active widgets.
Our widgets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft
from workspaces.story import story
from handlers.layout_widgets import top_pin, left_pin, right_pin, bottom_pin


# Will add our active widgets
# Needs to be outside so other widgets can call on it to update controls
widgets_row = ft.Row(
    spacing=4,
    expand=True,
    controls=story.active_widgets 
)



class ResizableWidget(ft.Container):
    def __init__(self, content):
        super().__init__(content=content)
        # Add drag handles as controls around the widget
        # Handle mouse events to resize
        print("nothing")


# Function to return our container for our widgets
def create_widgets(page: ft.Page):     

    


    # Format our pins and main work area into a column for our container
    column = ft.Column(
        spacing=4,
        expand=True,
        controls=[
            top_pin,
            ft.Row(expand=True, spacing=0, controls=[left_pin, widgets_row, right_pin]),
            bottom_pin,
        ]
    )

    # Container for 1 or more widgets open on the workspace area right side of screen
    active_widgets_container = ft.Container(
        expand=True,
        margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_800,
        content=column
    )
    

    return active_widgets_container