import flet as ft
from handlers.reload_widgets import reload_widgets
from handlers.layout_widgets import widget_row, drag_targets, stack


# Creates our new widget. All widgets fit into this standard format
def create_new_widget(title, body, story, page):


    # Hides our widgets when x is clicked in top right
    def hide_widget(story):

        # Make our widget false
        for idx, character in enumerate(story.characters):
            if character.name == title:
                character.visible = False
                story.visible_widgets[idx] = None
                print(title, "widget removed from visible widgets")

        # reload widgets
        reload_widgets(story)  # This will update the widgets in the story
        page.update()

    def on_drag_start(e):
        print("\ndrag start called")
        stack.controls.extend(drag_targets)  # Add the drag target pins to the stack
        stack.update()

    def on_drag_complete(e):    # Has no cancellation method, meaning errors if not dropped in workspace
        print("Drag complete called")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()


    
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
                            on_click=lambda e, : hide_widget(story),
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
