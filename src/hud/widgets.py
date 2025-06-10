'''
Our 'pagelets' page that returns the container for
all the active pagelets.
Our pagelets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft

def create_widgets(page: ft.Page):

    d1 = ft.Draggable(
        content=ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.Text(value="container 1", expand=True,)
        )
    )
    d2 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            #expand=True,
            width=20,
            bgcolor=ft.Colors.GREY_900,
            content=ft.ListView([ft.Text(value="container 2 is a really fun container that should probably quit being so difficult")])
        ),
    )
    d3 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.Text(value="container 3  so difficult")
        ),
    )
    d4 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.Text(value="container 4")
        ),
        content_feedback=ft.Container(  # Whats shown when dragging
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            width=100,
            height=100,
            bgcolor=ft.Colors.GREY_900,
        )
    )

    list = [d1, d2, d3, d4]

    gv = ft.GridView(
        #expand=True,
        controls=list,
        #runs_count=2,
        runs_count=len(list) // 2   # Set our runs count for grid formatting
    )
    # Main work area stuff in here
    main_work_area_container = ft.Container(
        expand=True, 
        bgcolor=ft.Colors.GREY_800, 
        content=ft.Column(
            expand=True, 
            controls=[
                ft.Row(
                    expand=True,
                    wrap=True,      # elements will move down a line if they dont fit
                    controls=[gv],  # List of draggables
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
    widgets_container = ft.Container(
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
                    scroll=None,
                    controls=[left_column, main_work_area_container, right_column]
                ),
                bottom_row,
            ]
        )
    )
    

    return widgets_container