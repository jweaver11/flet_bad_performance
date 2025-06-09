'''
Our 'pagelets' page that returns the container for
all the active pagelets 
'''

import flet as ft

def create_pagelets(page: ft.Page):


    c1 = ft.Container(
        expand=True,
        height=100,
        bgcolor=ft.Colors.BLUE_900,
        col={"xs": 12, "md": 6, "lg": 3},
        content=ft.Text("container 1")
    )
    c2 = ft.Container(
        expand=True,
        bgcolor=ft.Colors.YELLOW_900,
        col={"xs": 12, "md": 6, "lg": 3},
        content=ft.Text("container 2")
    )
    c3 = ft.Container(
        expand=True,
        bgcolor=ft.Colors.RED_900,
        col={"xs": 12, "md": 6, "lg": 3},
        content=ft.Text("container 3")
    )
    c4 = ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLUE_900,
        col={"xs": 12, "md": 6, "lg": 3},
        content=ft.Text("container 4")
    )
    c5 = ft.Container(
        expand=True,
        bgcolor=ft.Colors.YELLOW_900,
        height=200,
        col={"xs": 12, "md": 6, "lg": 3},
        content=ft.Text("container 5")
    )

    def page_resize(e):
        pw.value = f"{page.width} px"
        pw.update()

    page.on_resized = page_resize

    pw = ft.Text(bottom=50, right=50, style=ft.TextTheme.display_small)
    page.overlay.append(pw)

    rr = ft.ResponsiveRow(
        expand=True,
        spacing=4,
        #run_spacing=4,
        run_spacing={"xs": 10},
        controls=[c1, c2, c3, c4, c5]
    )
    
    # Container for 1 or more pagelets open on main right side of screen (work area)
    pagelets_container = ft.Container(
        expand=True,
        padding=10,
        border_radius=ft.border_radius.all(10),  # 20px radius on all corners
        #margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        bgcolor=ft.Colors.GREY_900,
        content=ft.Column([rr])
    )

    return pagelets_container