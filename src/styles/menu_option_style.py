# Style created for all our menu options, which are ft.buttons


import flet as ft

class Menu_Option_Style(ft.GestureDetector):
    def __init__(self, content: ft.Control, on_click: callable = None, data=None):
        super().__init__(
            expand=True,
            data=data,
            content=content,
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=on_click if on_click is not None else lambda e: None,
        )

   