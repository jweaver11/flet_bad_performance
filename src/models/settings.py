import flet as ft
from models.user import user

# Auto green characters = good, red = bad
# Checkbox labeled 'reorder_workspaces' that triggers the reorder event

# re-order the list of workspaces in the rail, show and hide them
'''
# Inside of workspaces rail to make reorderable or not,
# But will move here
# from hud.workspaces.rail import make_reorderable
ft.TextButton( 
    text="Reorder", 
    on_click=make_reorderable,
),
'''
# Snackbar alerts?


class Settings(ft.Container):
    def __init__(self):
        self.yo_momma = "yo mommaa"
        self.pin_location = "main"


        super().__init__(
            expand=True, 
            padding=6,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            bgcolor = ft.Colors.GREY_900,
            content=ft.TextButton("settings", on_click=lambda e: user.all_workspaces_rail.make_rail_reorderable()),

        )
