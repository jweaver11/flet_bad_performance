import flet as ft

class Snack_Bar(ft.SnackBar):
    def __init__(self, content: ft.Control):

        
        super().__init__(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            elevation=4,
            content=content,
            padding=None,
        )
        