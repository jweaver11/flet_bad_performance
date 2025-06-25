import flet as ft
from handlers.reload_widgets import reload_widgets

# Take our formatted widget from wherever it was created and make it a resizable widget
class ResizableWidget(ft.Container):
    def __init__(self, title, body, story, page):
        super().__init__()

        #page.update()


        # Add drag handles as controls around the widget
        # Handle mouse events to resize

    

# Just calls our resizable widget for readability
def create_new_widget(title, body, story, page):

    # Hides our widgets when x is clicked in top right
    def hide_widget(story):

        # Make our widget false
        for idx, character in enumerate(story.characters):
            if character.name == title:
                character.visible = False
                story.visible_widgets[idx] = None
                print(title, "widget removed from visible widgets")
            else:
                print("how you even get here?")
        
        # reload widgets
        reload_widgets(story)  # This will update the widgets in the story
        page.update()


    widget_container = ft.Container(
        expand=True,
        padding=6,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_900,
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
    #story = story
    #return ResizableWidget(title, body, story, page)


