# Style created for all our menu options, which are ft.buttons


import flet as ft

class Menu_Option_Style(ft.GestureDetector):
    def __init__(self, content: ft.Control, on_click: callable = None, data=None):
        super().__init__(
            #padding=ft.Padding(8, 4, 8, 4),
            #bgcolor=ft.Colors.ON_PRIMARY_CONTAINER,
            #border_radius=ft.border_radius.all(4),
            #padding=ft.Padding(6, 0, 0, 0),
            expand=True,
            data=data,
            content=content,
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=on_click if on_click is not None else lambda e: None,
        )

   