'''
Our 'pagelets' page that returns the container for
all the active pagelets 
'''

import flet as ft

def create_pagelets(page: ft.Page):
    # Container for 1 or more pagelets open on main right side of screen (work area)
    pagelets_container = ft.Container(
        expand=True,
        padding=10,
        border_radius=ft.border_radius.all(10),  # 20px radius on all corners
        #margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        bgcolor=ft.Colors.GREY_900,
        content=ft.Row(
            controls=[
                ft.Column(controls=[ft.Text("Pagelets container")])
            ]
        )
    )

    return pagelets_container