import flet as ft

# Give a default height
class ResizableWidget(ft.Container):
    def __init__(self, title, body, story):
        super().__init__(
            expand=True,
            padding=6,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            bgcolor=ft.Colors.GREY_900,
            visible=True,
            content=ft.Column(spacing=0, controls=[
                ft.Stack([
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[ft.Draggable(group="widgets", content=ft.TextButton(title))]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.IconButton(
                                on_click=lambda e, self=self: hide_widget(self, story),
                                icon=ft.Icons.CLOSE_ROUNDED
                    )])
                ]),
                ft.Divider(color=ft.Colors.BLUE),
                ft.Container(       # Body of the widget
                    expand=True,
                    content=ft.Column(body) 
                )
            ]) 
        )

        def hide_widget(widget, story):
            widget.visible = False
            # reload widgets
            story.reload_widgets

            print(" do something")

        # Add drag handles as controls around the widget
        # Handle mouse events to resize
        #print("nothing")


# Just calls our resizable widget for readability
def create_new_widget(title, body, story):
    return ResizableWidget(title, body, story)


