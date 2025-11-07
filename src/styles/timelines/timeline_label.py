# Class for labels of plot points and arcs used underneath timeline and arc dropdowns
import flet as ft

class Timeline_Label(ft.GestureDetector):
    def __init__(
        self, 
        title: str,
        icon: ft.Icon
    ):

        self.title = title
        self.icon = icon
        super().__init__(
            mouse_cursor=ft.MouseCursor.CLICK,
        )

        self.reload()


    def reload(self):
        self.content = ft.Container(
            alignment=ft.alignment.center,                  # Center within parent
            padding=ft.padding.only(right=10),             # Offset the indentation so we are centered
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,      # Center children
                controls=[
                    #ft.Icon(self.icon, color=ft.Colors.PRIMARY, size=16),
                    ft.Text(self.title, weight=ft.FontWeight.BOLD),
                ],
            ),
        )



            

    