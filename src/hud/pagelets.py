'''
Our 'pagelets' page that returns the container for
all the active pagelets.
Our pagelets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft

def create_pagelets(page: ft.Page):

    d1 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.Text("container 1")
        ),
    )
    d2 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.Text("container 2 is a really fun container that should probably quit being so difficult")
        ),
    )
    d3 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.Text("container 2 is a really fun container that should probably quit being so difficult")
        ),
    )
    list = [d1, d2, d3]

    # Main work area stuff in here
    main_work_area_container = ft.Container(
        expand=True, 
        bgcolor=ft.Colors.GREY_800, 
        content=ft.Column(
            expand=True, 
            controls=[
                ft.Row(
                    expand=True,
                    wrap=True,
                    controls=list,
                )
            ]
        )
    )

   
   # Our drag targets to format pagelets different ways
    top_row = ft.DragTarget(
        content=ft.Placeholder(
            expand=True,
            fallback_height=50,
        )
    )
    left_column = ft.DragTarget(
        content=ft.Placeholder(
            fallback_width=50,
        )
    )
    right_column = ft.DragTarget(
        content=ft.Placeholder(
            fallback_width=50,
        )
    )
    bottom_row = ft.DragTarget(
        content=ft.Placeholder(
            fallback_height=50,
        )
    )

    
    # Container for 1 or more pagelets open on main right side of screen (work area)
    pagelets_container = ft.Container(
        expand=True,
        margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_700,
        content=ft.Column(
            expand=True,
            controls=[
                top_row,
                ft.Row( # Mid row
                    expand=True,
                    controls=[left_column, main_work_area_container, right_column]
                ),
                bottom_row,
            ]
        )
    )
    

    return pagelets_container