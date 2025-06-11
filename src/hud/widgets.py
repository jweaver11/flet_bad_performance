'''
Our 'pagelets' page that returns the container for
all the active pagelets.
Our pagelets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft

def create_widgets(page: ft.Page):

    # Template for widget
    d1 = ft.Container(
        expand=True,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_900, 
        content=ft.Column([
            ft.Container(
                border_radius=ft.border_radius.all(10),  # 10px radius on all corners
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Draggable(
                    content=ft.TextButton("Container 1 Title"), 
                    content_feedback=ft.TextButton("Container 1 Title")
                )   
            ),
            ft.Container(content=ft.Text("Container 1 body"))
        ])
    )
    d2 = ft.Container(
        expand=True,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_900, 
        content=ft.Column([
            ft.Container(
                border_radius=ft.border_radius.all(10),  # 10px radius on all corners
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Draggable(
                    content=ft.TextButton("Container 2 Title"), 
                    content_feedback=ft.TextButton("Container 2 Title")
                )   
            ),
            ft.Container(content=ft.Text("Container 2 body"))
        ])
    )
    d3 = ft.Container(
        expand=True,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_900, 
        content=ft.Column([
            ft.Container(
                border_radius=ft.border_radius.all(10),  # 10px radius on all corners
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Draggable(
                    group="target",
                    content=ft.TextButton("Container 3 Title"), 
                    content_feedback=ft.TextButton("Container 3 Title")
                )   
            ),
            ft.Container(content=ft.Text("Container 3 body"))
        ])
    )
        
    # When draggable is dragged onto target
    def drag_will_accept(e):
        e.control.content.border = ft.border.all(
            2, ft.Colors.BLACK45 if e.data == "true" else ft.Colors.RED
        )
        e.control.update()

    # When user 'drops' draggable onto target
    def drag_accept(e: ft.DragTargetEvent):
        #src = page.get_control(f"{e.src_id}")
        #e.control.content.bgcolor = src.content.bgcolor
        #e.control.content.border = None
        print("drag accepted")
        tr_list.append(d3)
        e.control.update()
        page.update()

    # When draggable moves within its target
    def on_move(e):
        print("Draggable moved within target")

    # When draggable leaves target
    def drag_leave(e):
        e.control.content.border = None
        e.control.update()

    list = [d1, d2, d3]
    tr_list = []
    lc_list = []
    mr_list = []
    rc_list = []
    br_list = []

  
   # Our drag targets to format pagelets different ways
   # Make placeholders containers with rr's?
    top_row = ft.DragTarget(
        group="target",
        on_will_accept=drag_will_accept,
        on_accept=drag_accept,
        #on_move=on_move,
        on_leave=drag_leave,
        content=ft.Row(height=100, controls=tr_list)
    )
    # Replace placeholder with column??
    left_column = ft.DragTarget(
        group="target",
        content=ft.Placeholder(
            fallback_width=50,
        )
    )
    middle_row = ft.DragTarget(
        group="target",
        content=ft.ResponsiveRow(
            col={"xs": 2, "sm": 2, "md": 2, "lg": 2,}, 
            controls=list,
        )
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