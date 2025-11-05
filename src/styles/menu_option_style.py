# Style created for all our menu options, which are ft.buttons


import flet as ft

class Menu_Option_Style(ft.GestureDetector):
    def __init__(self, content: ft.Control, on_click: callable = None, data=None):
        super().__init__(
            expand=True,
            data=data,
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=on_click if on_click is not None else lambda e: None,
            on_enter=self.on_hover,
            on_exit=self.on_hover_exit,
            content=ft.Container(
                border_radius=ft.border_radius.all(6), 
                content=content
            ),
        )

    def on_hover(self, e: ft.HoverEvent):
        ''' Changes background color on hover '''
        
        self.content.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE_VARIANT)
        
        self.content.update()

    def on_hover_exit(self, e: ft.HoverEvent):
        ''' Resets background color on hover exit '''
        
        self.content.bgcolor = None
        
        self.content.update()

   