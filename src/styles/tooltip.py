import flet as ft


class Tooltip(ft.Tooltip):
    def __init__(self, tip: str):
        super().__init__(
            message=tip, 
            enable_feedback=True, 
            bgcolor=ft.Colors.ON_INVERSE_SURFACE,
            text_style=ft.TextStyle(color=ft.Colors.ON_SURFACE),
            border=ft.border.all(1, ft.Colors.OUTLINE),
            shadow=ft.BoxShadow(color=ft.Colors.BLACK, blur_radius=1, blur_style=ft.ShadowBlurStyle.NORMAL),
            padding=ft.padding.only(left=6, right=6),
            wait_duration=700,
        )
