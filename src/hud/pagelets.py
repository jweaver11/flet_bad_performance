'''
Our 'pagelets' page that returns the container for
all the active pagelets.
Our pagelets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft

def create_pagelets(page: ft.Page):

    d1 = ft.Draggable(
        group=1,
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.Text("container 1")
        ),
    )
    d2 = ft.Draggable(
        group=1,
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            height=200,
            width=200,
            bgcolor=ft.Colors.GREY_900,
            content=ft.Text("container 2")
        ),
        content_feedback=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            height=200,
            width=200,
            bgcolor=ft.Colors.GREY_900,
            content=ft.Text("container 2")
        ),
    )
   
   # Our drag targets to format pagelets different ways
    top_row = ft.DragTarget(
        content=ft.Placeholder(
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
        content=ft.ResponsiveRow(
            controls=[
                ft.Column(
                    controls=[
                        top_row,
                        ft.Row(
                            expand=True,
                            controls=[
                                left_column,
                                d1,
                                d2,
                                ft.Container(expand=True),
                                right_column,
                            ]
                        ),
                        bottom_row,
                    ]
                )
            ]
        )
    )
    

    return pagelets_container