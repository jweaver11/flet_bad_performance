'''
Our 'pagelets' page that returns the container for
all the active pagelets.
Our pagelets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft

def create_widgets(page: ft.Page):

    # Template for widget
    d1 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            # List view so scrolling enabled
            content=ft.ListView([ft.Text(value="container 1 is a really fun")]) 
        ),
        content_feedback=ft.Container(  # Whats shown when dragging
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            width=100,
            height=100,
            bgcolor=ft.Colors.GREY_900,
        )
    )
    d2 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.ListView([ft.Text(value="container 2 is a really fun")])
        ),
        content_feedback=ft.Container(  # Whats shown when dragging
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            width=100,
            height=100,
            bgcolor=ft.Colors.GREY_900,
        )
    )
    d3 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.ListView([ft.Text(value="container 3 is a really fun")])
        ),
        content_feedback=ft.Container(  # Whats shown when dragging
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            width=100,
            height=100,
            bgcolor=ft.Colors.GREY_900,
        )
    )
    d4 = ft.Draggable(
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            content=ft.ListView([ft.Text(value="container 4 is a really fun")])
        ),
        content_feedback=ft.Container(  # Whats shown when dragging
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            width=100,
            height=100,
            bgcolor=ft.Colors.GREY_900,
        )
    )

    list = [d1, d2, d3, d4]
    tr_list = []
    lc_list = []
    mr_list = []
    rc_list = []
    br_list = []


    # Not filling up cgc correctly, need better login on
    # child aspect ratio
    # Need gv to Fill up parent container without having to scroll - cgc
    # Give correct number of runs
    gv = ft.GridView(
        controls=list,
        child_aspect_ratio=16/9,
        runs_count=len(list) // 2   # Set our runs count for grid formatting
    )

  
   # Our drag targets to format pagelets different ways
   # Make placeholders containers with rr's?
    top_row = ft.DragTarget(
        group="top-row",
        content=ft.Placeholder(
            expand=True,
            fallback_height=50,
        )
    )
    # Replace placeholder with column??
    left_column = ft.DragTarget(
        group="left-column",
        content=ft.Placeholder(
            fallback_width=50,
        )
    )
    middle_row = ft.DragTarget(
        group="middle-row",
        content=ft.ResponsiveRow(controls=list)
    )
    right_column = ft.DragTarget(
        group="right-column",
        content=ft.Placeholder(
            fallback_width=50,
        )
    )
    bottom_row = ft.DragTarget(
        group="bottom-row",
        content=ft.Placeholder(
            fallback_height=50,
        )
    )

    # central grid container
    middle_row_container = ft.Container(
        expand=True,
        bgcolor=ft.Colors.GREY_800, 
        content=ft.Column(expand=True, controls=[middle_row])
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
                top_row,    # Make rr
                ft.Row( # Mid row -- make rr
                    expand=True,
                    controls=[left_column, middle_row_container, right_column]
                ),
                bottom_row, # make rr
            ]
        )
    )
    

    return widgets_container