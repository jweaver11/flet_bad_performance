'''
Our 'pagelets' page that returns the container for
all the active pagelets 
'''

import flet as ft

def create_pagelets(page: ft.Page):

    aspect_ratio = page.height / page.width     # aspect ratio for child containers

    def drag_will_accept(e):
        e.control.content.border = ft.border.all(
            2, ft.Colors.BLACK45 if e.data == "true" else ft.Colors.RED
        )
        e.control.update()

    def drag_accept(e: ft.DragTargetEvent):
        src = page.get_control(f"{e.src_id}")
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None
        e.control.update()

    def drag_leave(e):
        e.control.content.border = None
        e.control.update()

    d1 = ft.Draggable(
        content_when_dragging=None,
        content_feedback=None,
        group="color",
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            col={"xs": 12, "md": 6, "lg": 3},
            content=ft.Text("container 1")
        )
    )
    d2 = ft.Draggable(
        content_when_dragging=None,
        content_feedback=None,
        group="color",
        content=ft.Container(
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            expand=True,
            bgcolor=ft.Colors.GREY_900,
            col={"xs": 12, "md": 6, "lg": 3},
            content=ft.Text("container 2")
        )
    )

    # Our stack to hold our different pagelets
    pagelets_gv = ft.GridView(
        expand=True,
        runs_count=2,
        child_aspect_ratio=aspect_ratio,
        controls=[
            d1, 
            d2,
        ]
    )


    # Runs when page is resized - GRABS THE WHOLE PAGE, NOT PAGELETS PAGE
    def page_resize(e):
        pw.value = f"{page.width} px"
        pw.update()

    page.on_resized = page_resize


    pw = ft.Text(top=20, left=20, style=ft.TextTheme.display_small)
    page.overlay.append(pw)

    
    # Container for 1 or more pagelets open on main right side of screen (work area)
    pagelets_container = ft.Container(
        expand=True,
        border_radius=ft.border_radius.all(10),
        # alignment=ft.alignment.center,
        margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        content=pagelets_gv
    )
    

    return pagelets_container