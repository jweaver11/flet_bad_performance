""" WIP """

import flet as ft


def create_content_rail(page: ft.Page) -> ft.Control:
    
    return ft.Column(
        controls=[
            ft.TextButton(  # 'Create Character button'
                "Chapters", 
                icon=ft.Icons.WAVES_OUTLINED, 
            ),
            ft.TextButton(  # 'Create Character button'
                "Stuff", 
                icon=ft.Icons.WAVES_OUTLINED, 
            ),
            ft.TextButton(  # 'Create Character button'
                "More stuff", 
                icon=ft.Icons.WAVES_OUTLINED, 
            ),
            ft.Text("hi there")
        ]
    )
