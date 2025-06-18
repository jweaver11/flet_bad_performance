import flet as ft

# Give a default height
class ResizableWidget(ft.Container):
    def __init__(self, title, body):
        super().__init__(
            expand=True,
            padding=6,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            bgcolor=ft.Colors.GREY_900,
            visible=True,
            content=ft.Column([
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Draggable(
                        group="widgets", 
                        content=ft.TextButton(title)    # Title for the widget
                    )
                ]
            ),
            ft.Container(       # Body of the widget
                expand=True,
                content=ft.Column(body) 
            )
            ]) 
        )

        # Add drag handles as controls around the widget
        # Handle mouse events to resize
        #print("nothing")

# Just calls our resizable widget for readability
def new_widget(title, body):

    return ResizableWidget(title, body)