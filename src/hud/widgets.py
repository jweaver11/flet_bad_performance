'''
Our 'pagelets' page that returns the container for
all the active pagelets.
Our pagelets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft

def create_widgets(page: ft.Page):

    # When new widget pops out, format it to fit correctly
    def create_new_widget(title, body):
        widget_container = ft.Container(
            expand=True,
            padding=6,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            bgcolor=ft.Colors.GREY_900,
            content=ft.Column([
                ft.Row(     # Title of the widget
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.TextButton(title)]
                ),
                ft.Container(       # Body of the widget
                    expand=True,
                    content=ft.Column([ft.Row(wrap=True, controls=[ft.Text(body)])]) 
                )
            ])
        )
        return widget_container
    
        
    # list for active widgets in the workspace area
    d1 = create_new_widget("widget 1 title", "widget 1 body")
    d2 = create_new_widget("widget 2 title", "widget 2 body")
    d3 = create_new_widget("widget 3 title", "widget 3 body")

    active_widgets_list = [d1, d2, d3, create_new_widget("widget 4 title", "widget 4 body")]

    widgets_row = ft.Row(
        run_spacing = 10,
        spacing=10,
        expand=True,
        controls=active_widgets_list
    )

    tr = ft.Container(
        height=100,
        expand=True, 
        bgcolor=ft.Colors.RED,
        content=ft.Draggable(
            group="top_row",
            content=ft.Container(height=20)
        )
    )

    stack = ft.Stack(
        clip_behavior=True,
        controls=
        [
            d1, 
            d2,
            d3, 
            tr,
        ],
    )

    # Container for 1 or more pagelets open on main right side of screen (work area)
    active_widgets_container = ft.Container(
        expand=True,
        margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_800,
        content=widgets_row
    )
    

    return active_widgets_container