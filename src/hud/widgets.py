'''
Just the formatting for our 'widgets' workspace area.
Returns our container with our formatting areas inside the workspace area.
Formatted areas are: top pin, left pin, main work area, right pin, and bottom pin
'''

import flet as ft
from handlers.layout_widgets import top_pin, left_pin, main_work_area, right_pin, bottom_pin


# Function to return our container for our widgets
def create_widgets(page: ft.Page):     
    
    # Format our pins and main work area into a column for our container
    column = ft.Row(
        spacing=10,
        expand=True,
        controls=[
            left_pin,
            ft.Column(expand=True, spacing=10, controls=[top_pin, main_work_area, bottom_pin]),
            right_pin,
        ]
    )

    # Container for 1 or more widgets open on the workspace area right side of screen
    active_widgets_container = ft.Container(
        expand=True,
        margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        #bgcolor=ft.Colors.GREY_800,
        content=column
    )
    

    return active_widgets_container