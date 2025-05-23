''' Menu bar at the top of the page '''
import flet as ft


appbar_text_ref = ft.Ref[ft.Text]()


menubar = ft.MenuBar(
    expand=True,
    style=ft.MenuStyle(
        alignment=ft.alignment.top_left,
        bgcolor=ft.Colors.RED_300,
        mouse_cursor={
            ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
            ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
        },
    ),
)