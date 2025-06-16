'''
Our 'widgets' page that returns the container for
all the active widgets.
Our widgets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft
from workspaces.story import story



def create_widgets(page: ft.Page):      

    cont = ft.Container(
        expand=True,
        padding=6,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_900,
        content=ft.Column([
            ft.Row(     # Title of the widget
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[ft.TextButton("Title 1")]
            ),
            ft.Container(       # Body of the widget
                expand=True,
                content=ft.Column([ft.Row(wrap=True, controls=[ft.Text("Title 2")])]) 
            )
        ])
    )  

    story.active_widgets = cont

    # Will add our active widgets
    widgets_row = ft.Row(
        spacing=4,
        expand=True,
        controls=[story.active_widgets]
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