'''
Our 'widgets' page that returns the container for
all the active widgets.
Our widgets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft
from workspaces.story import story


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


# Format my layout for all the widgets
def layout_widgets(widgets):
    if len(widgets) == 1:
        return widgets[0]
    elif len(widgets) == 2:
        return ft.Row([widgets[0], widgets[1]], expand=True)
    elif len(widgets) == 3:
        return ft.Column([
            ft.Row([widgets[0], widgets[1]], expand=True),
            widgets[2]
        ], expand=True)
    # ... extend for more widgets



# Function to return our container for our widgets
def create_widgets(page: ft.Page):     

    def drag_accept(e):
        print("accepted")

    # AI stuff
    main_area = ft.Column(expand=True)
    top_pin = ft.DragTarget(group="widgets", content=ft.Container(height=50, bgcolor=ft.Colors.GREY_600))
    left_pin = ft.DragTarget(group="widgets", content=ft.Container(width=50, bgcolor=ft.Colors.GREY_600))
    right_pin = ft.DragTarget(group="widgets", content=ft.Container(width=50, bgcolor=ft.Colors.GREY_600))
    bottom_pin = ft.DragTarget(group="widgets", content=ft.Container(height=50, bgcolor=ft.Colors.GREY_600))

    widget = ft.Draggable(
        group="widgets",
        content=ft.Container(
            content=ft.Text("Widget 1"),
            bgcolor=ft.Colors.BLUE_200,
            padding=10,
            border_radius=10,
        )
    )

    main_area.controls.append(widget)


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