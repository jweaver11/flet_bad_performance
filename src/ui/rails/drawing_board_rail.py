""" WIP """

import flet as ft
from models.story import Story

def create_drawing_board_rail(page: ft.Page, story: Story=None) -> ft.Control:
    return ft.Column(
        controls=[
            ft.TextButton(  # 'Create Character button'
                "Drawing Board",  
            ),
            ft.Text("This is the drawing board rail")
        ]
    )