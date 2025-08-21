import flet as ft


def create_world_building_rail(page: ft.Page) -> ft.Control:
    
    return ft.Column(
        controls=[
            ft.TextButton("Geography", icon=ft.Icons.MAP),
            ft.TextButton("History", icon=ft.Icons.HISTORY),
            ft.Text("World Building Content Here")
        ]
    )

# Description of world
# Power systems (if any)
# Social systems
# Geography
# History/Timeline
# ...
