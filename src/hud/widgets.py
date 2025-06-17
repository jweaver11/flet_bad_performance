'''
Our 'widgets' page that returns the container for
all the active widgets.
Our widgets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft
from workspaces.story import story

def update_page(page):
    print("page updated")
    page.update()

# Class for widget objects in each story 
class Widget(ft.Container):

    def __init__(self, title):
        super().__init__(
        # Build our container
            expand=True,
            padding=6,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            bgcolor=ft.Colors.GREY_900,
            content=ft.Column([
                ft.Row(     # Title of the widget
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.TextButton(title)]
                ),
                ft.Container(       # Body of the widget
                    expand=True,
                    content=ft.Column([ft.Row(wrap=True, controls=[ft.Text(title)])]) 
                )
            ])
        )

active_widgets_list = [Widget("title 1"), Widget("title 2")]
story.active_widgets["char1"] = "char1 title"
story.active_widgets["char2"] = "char2 title"

def reload_widgets(page):
    active_widgets_list.clear()
    for widget in story.active_widgets:
        container = Widget(widget)
        active_widgets_list.append(container)
        print(story.active_widgets)
    update_page(page)
    return active_widgets_list

def create_widgets(page: ft.Page):      

    # Will add our active widgets
    widgets_row = ft.Row(
        spacing=4,
        expand=True,
        controls=active_widgets_list
    )

    # Container for 1 or more pagelets open on main right side of screen (work area)
    active_widgets_container = ft.Container(
        expand=True,
        margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_800,
        content=widgets_row
    )

    '''
    tr = ft.Container(
        height=100,
        expand=True, 
        bgcolor=ft.Colors.RED,
        content=ft.DragTarget(
            group="top_row",
            content=ft.Container(height=20)
        )
    )

    stack = ft.Stack(
        clip_behavior=True,
        controls=
        [
            #d1, 
            #d2,
            #tr,
        ],
    )
    '''

    return active_widgets_container