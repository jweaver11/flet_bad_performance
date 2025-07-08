import flet as ft
from models.story import story
from handlers.render_widgets import render_widgets, widget_row, pin_drag_targets, stack
from handlers.arrange_widgets import arrange_widgets


# Creates our widget from passing in the object, page, and formatting
def create_widget(obj, page):

    title = obj.title
    tag = obj.tag
    pin_location = obj.pin_location

    body = obj.body

    # Hides our widgets when x is clicked in top right
    def hide_widget(obj):


        print("pin location: ", obj.pin_location)

        if obj.pin_location == "top":
            for obj in story.top_pin_obj:
                if obj.title == title:
                    obj.visible = False
                    print(title, " is visible: ", obj.visible)

        if obj.pin_location == "left":
            for obj in story.left_pin_obj:
                if obj.title == title:
                    obj.visible = False
                    print(title, " is visible: ", obj.visible)

        if obj.pin_location == "main":
            for obj in story.main_pin_obj:
                if obj.title == title:
                    obj.visible = False
                    print(title, " is visible: ", obj.visible)
                
        if obj.pin_location == "right":
            for obj in story.right_pin_obj:
                if obj.title == title:
                    obj.visible = False
                    print(title, " is visible: ", obj.visible)

        if obj.pin_location == "bottom":
            for obj in story.bottom_pin_obj:
                if obj.title == title:
                    obj.visible = False
                    print(title, " is visible: ", obj.visible)

        
        # elif dif pin locatin...
        arrange_widgets()  # Re-arrange widgets after hiding one
        render_widgets(page)
        page.update()

    def on_drag_start(e):
        print("\ndrag start called\n")

        stack.controls.extend(pin_drag_targets)  # Add the drag target pins to the stack
        stack.update()

    def on_drag_complete(e):    # Has no cancellation method, meaning errors if not dropped in workspace
        print("Drag complete called")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()


    # When we render the body, we take from the 'body' attribute of the object, and the 'title'

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
                        data=obj,       # Pass our object as the data so we can access it
                        on_drag_start=on_drag_start,
                        on_drag_complete=on_drag_complete,)]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.IconButton(
                            on_click=lambda e: hide_widget(obj),
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

