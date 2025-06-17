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

# Function to return our container for our widgets
def create_widgets(page: ft.Page):      

    tr = ft.Container(  # top row drag target
        bgcolor=ft.Colors.GREY_900,
        content=ft.DragTarget(
            group="top_row",
            content=ft.Container(height=20)
        )
    )
    lc = ft.Container(  # left column drag target
        bgcolor=ft.Colors.GREY_900,
        content=ft.DragTarget(
            group="left_column",
            content=ft.Container(width=20)
        )
    )
    rc = ft.Container(   # right column drag target
        bgcolor=ft.Colors.GREY_900,
        content=ft.DragTarget(
            group="right_column",
            content=ft.Container(width=20)
        )
    )

    br = ft.Container(   # bottom row drag target
        bgcolor=ft.Colors.GREY_900,
        content=ft.DragTarget(
            group="bottom_row",
            content=ft.Container(height=20)
        )
    )

    column = ft.Column(
        spacing=4,
        expand=True,
        controls=[
            tr,
            ft.Row(expand=True, spacing=0, controls=[lc, widgets_row, rc]),
            br,
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