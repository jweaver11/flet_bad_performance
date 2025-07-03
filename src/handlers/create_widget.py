import flet as ft
from models.story import story
from handlers.render_widgets import render_widgets, widget_row, pin_drag_targets, stack


# Creates our widget from passing in the object, page, and formatting
def create_widget(obj, page):

    title = obj.title
    tag = obj.tag
    pin_location = obj.pin_location

    body = obj.body

    # Hides our widgets when x is clicked in top right
    def hide_widget(e):

        if pin_location == "bottom":
            for obj in story.bottom_pin_obj:
                if obj.title == title:
                    obj.visible = False
                    print(title, " is visible: ", obj.visible)

        
        # elif dif pin locatin...
        page.update()
        render_widgets(page)

    def on_drag_start(e):
        print("\ndrag start called")

        stack.controls.extend(pin_drag_targets)  # Add the drag target pins to the stack
        stack.update()

    def on_drag_complete(e):    # Has no cancellation method, meaning errors if not dropped in workspace
        print("Drag complete called")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()


    # Render body seperately, heder the same?

    # Our container that returns the 'control' for the widget
    widget_container = ft.Container(
        expand=True,
        padding=6,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_900,
        content=ft.Column(spacing=0, controls=[
            ft.Stack([
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Draggable(
                        group="widgets",
                        content=ft.TextButton(title),
                        on_drag_start=on_drag_start,
                        on_drag_complete=on_drag_complete,)]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.IconButton(
                            on_click=hide_widget,
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

    return widget_container

