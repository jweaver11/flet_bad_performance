""" WIP """

import flet as ft

def create_drawing_board_rail(page: ft.Page) -> ft.Control:
    return ft.Column(
        controls=[
            ft.TextButton(  # 'Create Character button'
                "Drawing Board",  
            ),
            ft.Text("This is the drawing board rail")
        ]
    )