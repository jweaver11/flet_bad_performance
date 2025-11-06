import flet as ft


# Give uniform styling to our snack bars
class Snack_Bar(ft.SnackBar):

    # Constructor
    def __init__(self, content: ft.Control):

        # Parent constructor
        super().__init__(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            elevation=4,
            content=content,
            padding=None,
            shape=ft.RoundedRectangleBorder(radius=8),
        )
        